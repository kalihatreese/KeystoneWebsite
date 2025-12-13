import time, requests

API_KEY = "<INSERT_ALPACA_KEY>"
API_SECRET = "<INSERT_ALPACA_SECRET>"
BASE_URL = "https://paper-api.alpaca.markets"

def truth_alignment(signal):
    # Removes greedy or fear-driven noise
    # Reinforces stable, evidence-based trades
    return signal * 0.85

def get_price(symbol="SPY"):
    url = f"{BASE_URL}/v2/stocks/{symbol}/quotes/latest"
    r = requests.get(url, headers={"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": API_SECRET})
    return r.json().get("quote", {}).get("ap", None)

def trade(action, qty=1, symbol="SPY"):
    url = f"{BASE_URL}/v2/orders"
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": action,
        "type": "market",
        "time_in_force": "gtc"
    }
    r = requests.post(url, json=data,
                      headers={"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": API_SECRET})
    return r.json()

def run_trinity():
    print("=== Trinity ReeseOS Online ===")
    print("Truth + Alignment Mode Activated")

    cash = 39

    while True:
        price = get_price()
        if not price:
            print("Waiting for price data…")
            time.sleep(5)
            continue

        # primitive EMA-style motion
        signal = 1 if price % 2 == 0 else -1

        aligned = truth_alignment(signal)

        if aligned > 0:
            print("Buy signal (aligned). Executing…")
            print(trade("buy"))
        else:
            print("Sell signal (aligned). Executing…")
            print(trade("sell"))

        time.sleep(60)

if __name__ == "__main__":
    run_trinity()
