import os
from dotenv import load_dotenv
from alpaca_trade_api import REST

load_dotenv()

api = REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL")
)

balance = api.get_account().equity
print("ACCOUNT EQUITY:", balance)

print("RapidAlpha-X and Trinity base layer initialized. This system is ready for manual command.")
