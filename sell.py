from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.enums import AssetClass

# ----- YOUR LIVE KEYS AS PROVIDED -----
API_KEY = "AKR2ENNYXBX4ZRK2E5RWC7LAMG"
SECRET_KEY = "Ctqb1sWWVG7GEhs25FrNBfgVBKa4LnanAaLvzhETtZCQ"

client = TradingClient(API_KEY, SECRET_KEY, paper=False)

# Fetch all positions
positions = client.get_all_positions()

for p in positions:
    if p.asset_class == AssetClass.CRYPTO:
        symbol = p.symbol
        qty = p.qty

        print(f"Selling {qty} of {symbol}")

        order = MarketOrderRequest(
            symbol=symbol,
            qty=float(qty),
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC,
        )

        client.submit_order(order)
        print(f"✔ Market sell submitted for {symbol}")

print("----- All crypto positions have been submitted for sale -----")
