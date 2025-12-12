from alpaca_trade_api.rest import REST
import os

# --- Set your API keys here ---
api_key = os.getenv('APCA_API_KEY_ID', 'YOUR_API_KEY')
secret_key = os.getenv('APCA_API_SECRET_KEY', 'YOUR_SECRET_KEY')
base_url = "https://paper-api.alpaca.markets"

api = REST(api_key, secret_key, base_url)

# Get account info
account = api.get_account()
cash = float(account.cash)

# Fetch all tradable crypto pairs
all_assets = api.list_assets()
crypto_pairs = [a.symbol for a in all_assets if getattr(a, 'class', '') == 'crypto' and a.tradable]

if not crypto_pairs:
    print("No tradable crypto pairs found. Exiting.")
    exit()

allocation = cash / len(crypto_pairs)

for symbol in crypto_pairs:
    try:
        bars = api.get_crypto_bars(symbol, '1D').df
        if bars.empty:
            print(f"No data returned for {symbol}, skipping.")
            continue

        last_price = float(bars['close'].iloc[-1])
        qty = round(allocation / last_price, 6)

        if qty * last_price < 1:  # minimum order amount requirement
            print(f"Order for {symbol} skipped: cost below minimum.")
            continue

        # Submit market buy order
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side="buy",
            type="market",
            time_in_force="gtc"
        )
        print(f"Bought {qty} of {symbol} at ${last_price}")

    except Exception as e:
        print(f"Order failed for {symbol}: {e}")
