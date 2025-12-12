from alpaca_trade_api.rest import REST, TimeFrame
import os
import sys

# Load your API keys from environment variables
API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

# --- SANITY CHECK: Ensure keys were loaded ---
if not API_KEY or not SECRET_KEY:
    print("FATAL ERROR: API keys (APCA_API_KEY_ID or APCA_API_SECRET_KEY) not loaded from environment.")
    print("Please ensure they are correctly exported or defined in your shell before running.")
    sys.exit(1)
# ---------------------------------------------

# --- CRITICAL CHANGE: Using the Live Trading URL ---
BASE_URL = "https://api.alpaca.markets"  # This is the Live Trading URL
api = REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# Get account info (Authorization Test)
try:
    account = api.get_account()
    cash = float(account.cash)
except Exception as e:
    print(f"CRITICAL ERROR: Cannot access account. Authentication failed.")
    print(f"Alpaca API response: {e}")
    print("\n--- ACTION REQUIRED ---")
    print("Verify that your environment contains LIVE KEYS and not PAPER keys.")
    sys.exit(1)

# Fetch all tradable crypto assets
all_assets = api.list_assets()
crypto_pairs = [asset.symbol for asset in all_assets if asset.exchange == "CBSE" and asset.tradable]

if not crypto_pairs:
    print("No tradable crypto pairs found. Exiting.")
    sys.exit(0)

allocation = cash / len(crypto_pairs)

print(f"Successfully authenticated to LIVE Account: {account.account_number}")
print(f"Account Cash: ${cash:.2f}. Allocating ${allocation:.2f} per symbol.")

for symbol in crypto_pairs:
    try:
        bars = api.get_crypto_bars(symbol, TimeFrame.Hour).df 
        
        if bars.empty:
            print(f"No data returned for {symbol}, skipping.")
            continue

        last_price = float(bars['close'].iloc[-1])
        qty = round(allocation / last_price, 6)

        if qty * last_price < 1:
            print(f"Order for {symbol} skipped: cost below minimum ($1).")
            continue

        api.submit_order(
            symbol=symbol,
            qty=qty,
            side="buy",
            type="market",
            time_in_force="gtc"
        )
        print(f"Bought {qty} of {symbol} at ${last_price:.2f}")

    except Exception as e:
        print(f"Order failed for {symbol}: {e}")
