import os, time
from dotenv import load_dotenv
from alpaca_trade_api import REST
from strategy import trading_signal

load_dotenv()

api = REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL")
)

while True:
    bars = api.get_bars("AAPL", "1Min", limit=5)
    signal = trading_signal(bars)

    if signal == "BUY_CALL":
        api.submit_order(symbol="AAPL", qty=1, side="buy", type="market", time_in_force="gtc")
    elif signal == "BUY_PUT":
        api.submit_order(symbol="AAPL", qty=1, side="sell", type="market", time_in_force="gtc")

    time.sleep(60)
