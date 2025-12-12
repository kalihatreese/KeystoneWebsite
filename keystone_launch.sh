#!/bin/bash

# --- Set Alpaca Environment Variables ---
export ALPACA_API_KEY="AK74TVNAPD6UZBY7ZIPJI7GFIH"
export ALPACA_SECRET_KEY="Fg1dFkpFMfMA3jUcRTC3nQpKdCDpTAkcYiz33WjTiCd6"
export ALPACA_BASE_URL="https://api.alpaca.markets"

# --- Create Python Trading Script ---
cat << 'PYEOF' > launch_trades.py
import os
from alpaca_trade_api.rest import REST, TimeFrame
import time

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")
base_url = os.getenv("ALPACA_BASE_URL")

api = REST(api_key, secret_key, base_url)

symbol = "SPY"
qty = 1
target_profit = 1.5
stop_loss = 1.0
check_interval = 30

def wait_for_close(symbol):
    while True:
        try:
            position = api.get_position(symbol)
            print(f"Position still open: {position.qty} shares")
            time.sleep(check_interval)
        except:
            print(f"Position closed for {symbol}")
            break

def launch_trade(symbol, qty):
    try:
        order = api.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc')
        print("Buy order submitted:", order)
    except Exception as e:
        print("Buy order failed:", e)
        return
    while True:
        time.sleep(check_interval)
        try:
            position = api.get_position(symbol)
            current_price = float(position.current_price)
            entry_price = float(position.avg_entry_price)
            pnl_percent = (current_price - entry_price) / entry_price * 100
            print(f"{symbol} PnL: {pnl_percent:.2f}%")
            if pnl_percent >= target_profit or pnl_percent <= -stop_loss:
                api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='gtc')
                print(f"Trade exited at ${current_price} with PnL: {pnl_percent:.2f}%")
                break
        except:
            break

while True:
    launch_trade(symbol, qty)
    wait_for_close(symbol)
    print("Ready for next trade cycle.")
PYEOF

# --- Launch the Trading Script ---
python launch_trades.py
