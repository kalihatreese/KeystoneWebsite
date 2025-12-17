import os, sys, numpy as np
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

symbol = sys.argv[1]

api_key = os.getenv("ALPACA_API_KEY")
secret = os.getenv("ALPACA_SECRET_KEY")

client = StockHistoricalDataClient(api_key, secret)

req = StockBarsRequest(
    symbol_or_symbols=[symbol],
    timeframe=TimeFrame.Minute,
    limit=100
)

bars = client.get_stock_bars(req)[symbol]

closes = np.array([b.close for b in bars])

short = np.mean(closes[-20:])
long = np.mean(closes[-50:])

signal = short - long
print(signal)
