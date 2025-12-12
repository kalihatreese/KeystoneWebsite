from alpaca_trade_api.rest import REST

# Replace these with your actual API keys
API_KEY = "AK5IOUAW5SYI3L4JZAJMM4JIFW"
API_SECRET = "SecretG1C7mfqmtXubPE2gXVsDxY56s6jRRXEKx8NjEprXq8cp"
BASE_URL = "https://api.alpaca.markets"

api = REST(API_KEY, API_SECRET, base_url=BASE_URL)

# Check account info
try:
    account = api.get_account()
    print("Account ID:", account.id)
    print("Cash available:", account.cash)
    print("Buying power:", account.buying_power)
    print("Status:", account.status)
except Exception as e:
    print("Error fetching account:", e)

# List tradable crypto assets
try:
    assets = api.list_assets()
    crypto_pairs = [a.symbol for a in assets if a.exchange == "CBSE" and a.tradable]
    print("Tradable crypto pairs:", crypto_pairs)
except Exception as e:
    print("Error listing crypto assets:", e)
