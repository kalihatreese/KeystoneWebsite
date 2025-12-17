import os, sys
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

symbol = sys.argv[1]
strength = float(sys.argv[2])

api_key = os.getenv("ALPACA_API_KEY")
secret = os.getenv("ALPACA_SECRET_KEY")

client = TradingClient(api_key, secret, paper=True)

side = OrderSide.BUY if strength > 0 else OrderSide.SELL

order = MarketOrderRequest(
    symbol=symbol,
    qty=1,
    side=side,
    time_in_force=TimeInForce.DAY
)

client.submit_order(order)
print(f"[EXECUTE] Executed {side} on {symbol} (strength={strength})")
