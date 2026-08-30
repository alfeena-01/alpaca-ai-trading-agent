"""
Configuration file for the Alpaca Trading Agent.
Contains all adjustable parameters for the trading system.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== API CONFIGURATION ====================
APCA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
APCA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
APCA_API_BASE_URL = os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets")

# ==================== TRADING SYMBOLS ====================
# Symbols to monitor and trade
SYMBOLS = os.getenv("SYMBOLS_TO_TRADE", "AAPL,MSFT,GOOGL,TSLA,SPY").split(",")

# ==================== AGENT PARAMETERS ====================
# How often to check market (in seconds)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))

# Maximum daily loss before stopping all trading
MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", -5000))

# Risk tolerance per trade (as percentage of account)
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", 0.02))

# Minimum confidence threshold for signals (0.0 to 1.0)
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", 0.6))

# ==================== POSITION MANAGEMENT ====================
# Profit taking level (% gain)
PROFIT_TAKE_LEVEL = 0.02  # 2%

# Stop loss level (% loss)
STOP_LOSS_LEVEL = -0.015  # -1.5%

# Maximum positions to hold simultaneously
MAX_POSITIONS = 5

# ==================== TECHNICAL ANALYSIS ====================
# RSI Period
RSI_PERIOD = 14

# MACD Parameters
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bollinger Bands Period
BB_PERIOD = 20
BB_STD = 2

# SMA Periods
SMA_SHORT = 5
SMA_LONG = 20

# ==================== OPTIONS STRATEGY ====================
# Strike distance for spreads (as percentage of current price)
BULL_CALL_STRIKE_DISTANCE = 5
BULL_PUT_STRIKE_DISTANCE = 5

# Default expiration days
OPTION_EXPIRATION_DAYS = 30

# ==================== MARKET DATA ====================
# Timeframe for bar analysis
TIMEFRAME = "5Min"

# Number of bars to use for analysis
BARS_LIMIT = 100

# ==================== LOGGING ====================
LOG_FILE = "trading_agent.log"
TRADE_LOG_FILE = "trading_log.csv"

# ==================== MARKET HOURS ====================
# EST/EDT Market hours
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30
MARKET_CLOSE_HOUR = 16
MARKET_CLOSE_MINUTE = 0

# ==================== ALERT THRESHOLDS ====================
# Alert if P&L moves beyond these levels
ALERT_THRESHOLD_PROFIT = 1000  # $1000 profit
ALERT_THRESHOLD_LOSS = -500    # $500 loss

print("Configuration loaded successfully")
