from alpaca_trade_api.rest import REST, TimeFrame
import os

# Load your API keys from environment variables
API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"  # Use live URL if live trading

api = REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# Get account info
try:
    account = api.get_account()
    cash = float(account.cash)
except Exception as e:
    print(f"Cannot access account: {e}")
    exit(1)

# Fetch all tradable crypto assets
all_assets = api.list_assets()
crypto_pairs = [asset.symbol for asset in all_assets if asset.exchange == "CBSE" and asset.tradable]
if not crypto_pairs:
    print("No tradable crypto pairs found. Exiting.")
    exit(0)

allocation = cash / len(crypto_pairs)

for symbol in crypto_pairs:
    try:
        bars = api.get_crypto_bars(symbol, TimeFrame.Minute).df
        if bars.empty:
            print(f"No data returned for {symbol}, skipping.")
            continue

        last_price = float(bars['close'].iloc[-1])
        qty = round(allocation / last_price, 6)

        # Skip if below minimum order size ($1)
        if qty * last_price < 1:
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
