#!/usr/bin/env python3
"""
Confident Trader Module for KeystoneCreatorSuite
- Single-trade manager
- Reads keys automatically via Suite key_loader
- High-confidence entries only
"""

import os, time, math, json, datetime as dt
import pandas as pd, numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

# ===== CONFIG =====
TICKERS = ["AAPL","IBM","GOOGL","BTCUSD","ETHUSD","LAZR","CVNA","TMUS","COKE"]
FAST_EMA = 8
SLOW_EMA = 21
RSI_PERIOD = 14
RSI_MAX = 72
ATR_WINDOW = 14
VOL_PCT_FOR_AGGRO = 0.018

MIN_CONFIDENCE = 0.80
MIN_EXPECTED_RETURN = 0.03
POSITION_FRACTION_HUNT = 0.35
POSITION_FRACTION_AGGRO = 0.80
LOOKBACK_BARS = 400
LOOKAHEAD_MINUTES = 120
BAR_MINUTES = 1
MAX_HOLD_MINUTES = 240
SLEEP_BETWEEN_SCANS = 12
LOG_CSV = "keystone_confident_log.csv"
# ==================

# Keystone Suite key loader
try:
    from key_loader import load_keys
    API_KEY, API_SECRET, API_BASE = load_keys()
except Exception as e:
    print("Key loader failed:", e)
    raise SystemExit("Cannot continue without API keys")

from alpaca_trade_api.rest import REST, TimeFrame
api = REST(API_KEY, API_SECRET, API_BASE, api_version='v2')

# --- Logging ---
def log_event(d: dict):
    df = pd.DataFrame([d])
    log_path = os.path.join(os.path.dirname(__file__), LOG_CSV)
    if not os.path.exists(log_path):
        df.to_csv(log_path, index=False)
    else:
        df.to_csv(log_path, mode='a', header=False, index=False)
    print(json.dumps(d))

# --- Indicator functions ---
def fetch_bars(symbol, limit=LOOKBACK_BARS, timeframe=TimeFrame.Minute):
    try:
        bars = api.get_bars(symbol, timeframe, limit=limit).df
        if bars.empty:
            return None
        if isinstance(bars.index, pd.MultiIndex):
            bars = bars.xs(symbol, level=1)
        bars = bars.tz_convert(None)
        return bars
    except Exception as e:
        print("fetch_bars error", symbol, e)
        return None

def compute_indicators(df):
    close = df['close']
    fast = EMAIndicator(close, window=FAST_EMA).ema_indicator()
    slow = EMAIndicator(close, window=SLOW_EMA).ema_indicator()
    rsi = RSIIndicator(close, window=RSI_PERIOD).rsi()
    high, low, prev_close = df['high'], df['low'], close.shift(1)
    tr = pd.concat([high-low, (high-prev_close).abs(), (low-prev_close).abs()], axis=1).max(axis=1)
    atr = tr.rolling(ATR_WINDOW).mean()
    return fast, slow, rsi, atr

def mode_from_atr(close, atr):
    if atr is None or close == 0:
        return "hunt"
    vol_pct = atr / close
    return "aggro" if vol_pct >= VOL_PCT_FOR_AGGRO else "hunt"

def find_recent_crossover(fast, slow, window=3):
    if len(fast) < window+1:
        return False
    return (fast.iloc[-window-1] <= slow.iloc[-window-1]) and (fast.iloc[-1] > slow.iloc[-1])

def estimate_historical_edge(df):
    fast, slow, rsi, atr = compute_indicators(df)
    cross_indices = []
    for i in range(SLOW_EMA+20, len(df)-5):
        if (fast.iloc[i-3] <= slow.iloc[i-3]) and (fast.iloc[i] > slow.iloc[i]):
            cross_indices.append(i)
    if not cross_indices:
        return 0.0, 0.0
    forward_returns = []
    lookahead_bars = int(LOOKAHEAD_MINUTES / BAR_MINUTES)
    close = df['close'].values
    for idx in cross_indices:
        end_idx = min(idx + lookahead_bars, len(close)-1)
        window_high = df['high'].iloc[idx+1:end_idx+1].max()
        forward_ret = (window_high - close[idx]) / close[idx]
        forward_returns.append(forward_ret)
    avg = float(np.nanmean(forward_returns)) if forward_returns else 0.0
    hit_rate = float(np.mean([1 if r >= MIN_EXPECTED_RETURN else 0 for r in forward_returns])) if forward_returns else 0.0
    return avg, hit_rate

def calc_qty(cash, price, fraction):
    usd_to_use = cash * fraction
    qty = math.floor((usd_to_use / price) * 10000) / 10000.0
    if qty <= 0 and price < 1.0:
        qty = max(qty, 0.0001)
    return qty

# --- Trade functions ---
def place_buy_market(symbol, qty):
    try:
        return api.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc')
    except Exception as e:
        print("Buy order failed:", e)
        return None

def place_sell_market(symbol, qty):
    try:
        return api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='gtc')
    except Exception as e:
        print("Sell order failed:", e)
        return None

def available_cash():
    acct = api.get_account()
    return float(acct.cash)

def position_exists():
    positions = api.list_positions()
    return len(positions) > 0

def get_open_position(symbol):
    try:
        pos = api.get_position(symbol)
        return pos
    except Exception:
        return None

def monitor_position_and_exit(symbol, entry_price, mode, qty):
    profit_target = 0.08 if mode == "aggro" else 0.03
    stop_loss = 0.06 if mode == "aggro" else 0.015
    start_ts = dt.datetime.utcnow()
    print(f"Monitoring {symbol} entry {entry_price:.6f} qty {qty} mode {mode}")
    while True:
        try:
            bars = fetch_bars(symbol, limit=10)
            if bars is None:
                time.sleep(5); continue
            last_price = float(bars['close'].iloc[-1])
            pnl_pct = (last_price - entry_price) / entry_price
            elapsed_minutes = (dt.datetime.utcnow() - start_ts).total_seconds() / 60.0
            fast, slow, rsi, atr = compute_indicators(bars)
            ema_fast, ema_slow = fast.iloc[-1], slow.iloc[-1]
            exit_reason = None
            if pnl_pct >= profit_target:
                exit_reason = f"take_profit_{pnl_pct:.4f}"
            elif pnl_pct <= -stop_loss:
                exit_reason = f"stop_loss_{pnl_pct:.4f}"
            elif ema_fast < ema_slow:
                exit_reason = "ema_cross_down"
            elif elapsed_minutes >= MAX_HOLD_MINUTES:
                exit_reason = "max_hold_time"
            if exit_reason:
                print(f"Exiting {symbol} at {last_price:.6f} reason {exit_reason} pnl {pnl_pct:.4f}")
                place_sell_market(symbol, qty)
                log_event({
                    "timestamp": dt.datetime.utcnow().isoformat(),
                    "action": "exit",
                    "symbol": symbol,
                    "last_price": last_price,
                    "pnl_pct": pnl_pct,
                    "reason": exit_reason,
                    "mode": mode,
                    "qty": qty
                })
                return
            time.sleep(6)
        except Exception as e:
            print("monitor error", e)
            time.sleep(6)

def scan_and_trade_once():
    if not api.get_clock().is_open:
        print("Market closed; wait.")
        return
    if position_exists():
        print("Position exists; skip entry.")
        return
    cash = available_cash()
    if cash <= 1.0:
        print("Insufficient cash:", cash); return

    for sym in TICKERS:
        try:
            bars = fetch_bars(sym, limit=LOOKBACK_BARS)
            if bars is None or len(bars) < SLOW_EMA + 50:
                continue
            fast, slow, rsi, atr = compute_indicators(bars)
            latest_close = float(bars['close'].iloc[-1])
            latest_rsi = rsi.iloc[-1]
            latest_atr = atr.iloc[-1]
            if not find_recent_crossover(fast, slow, window=3):
                continue
            if latest_rsi >= RSI_MAX:
                continue
            avg_forward, hit_rate = estimate_historical_edge(bars)
            cross_freshness = 1.0 if (fast.iloc[-2] <= slow.iloc[-2] and fast.iloc[-1] > slow.iloc[-1]) else 0.6
            rsi_score = max(0.0, (70 - latest_rsi) / 30.0)
            vol_pct = (latest_atr / latest_close) if latest_close>0 else 0
            vol_score = min(1.0, vol_pct / VOL_PCT_FOR_AGGRO) if vol_pct>0 else 0.5
            edge_score = min(1.0, avg_forward / (MIN_EXPECTED_RETURN + 1e-9))
            combined = (0.30*cross_freshness) + (0.25*rsi_score) + (0.20*vol_score) + (0.25*edge_score)
            mode = mode_from_atr(latest_close, latest_atr)
            fraction = POSITION_FRACTION_AGGRO if mode=="aggro" else POSITION_FRACTION_HUNT
            print(f"{sym} -> combined_score={combined:.3f} avg_forward={avg_forward:.4f} hit_rate={hit_rate:.2f} mode={mode}")
            if combined >= MIN_CONFIDENCE and avg_forward >= MIN_EXPECTED_RETURN:
                qty = calc_qty(cash, latest_close, fraction)
                if qty <= 0:
                    continue
                print(f"CONFIDENT BUY {sym} qty {qty} approx_price {latest_close:.4f} score {combined:.3f}")
                buy_order = place_buy_market(sym, qty)
                if buy_order is None:
                    continue
                log_event({
                    "timestamp": dt.datetime.utcnow().isoformat(),
                    "action": "entry",
                    "symbol": sym,
                    "approx_price": latest_close,
                    "qty": qty,
                    "mode": mode,
                    "combined_score": combined,
                    "avg_forward": avg_forward,
                    "hit_rate": hit_rate
                })
                time.sleep(2)
                pos = None
                for _ in range(8):
                    pos = get_open_position(sym)
                    if pos: break
                    time.sleep(1)
                if not pos:
                    print("No position found after buy entry")
                    continue
                entry_price = float(pos.avg_entry_price)
                qty_held = float(pos.qty)
                monitor_position_and_exit(sym, entry_price, mode, qty_held)
                return
        except Exception as e:
            print("scan error", sym, e)
            continue

def run_confident_trader():
    print("Starting Keystone confident trader module...")
    while True:
        try:
            scan_and_trade_once()
            time.sleep(SLEEP_BETWEEN_SCANS)
        except KeyboardInterrupt:
            print("Interrupted by user"); break
        except Exception as e:
            print("Main loop error", e)
            time.sleep(5)

if __name__ == "__main__":
    run_confident_trader()
