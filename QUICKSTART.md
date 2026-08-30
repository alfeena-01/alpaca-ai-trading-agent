# Quick Start Guide - Alpaca AI Trading Agent

## 🚀 Get Started in 5 Minutes

### Step 1: Clone/Setup Project
```bash
cd c:\Users\User\OneDrive\Desktop\Alpaca
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Credentials
```bash
# Copy example
cp .env.example .env

# Edit .env with your Alpaca credentials:
# APCA_API_KEY_ID=your_key_here
# APCA_API_SECRET_KEY=your_secret_here
```

### Step 5: Run Agent
```bash
# Option A: Interactive startup menu
python startup.py

# Option B: Direct agent start
python agent.py

# Option C: Dashboard only (separate terminal)
streamlit run dashboard.py
```

---

## 📊 File Structure

| File | Purpose |
|------|---------|
| **agent.py** | Main autonomous trading agent |
| **strategy.py** | Trading signal generation & analysis |
| **utils.py** | Alpaca API wrapper & utilities |
| **dashboard.py** | Streamlit monitoring dashboard |
| **config.py** | Configuration parameters |
| **advanced_strategies.py** | Additional trading strategies |
| **startup.py** | Setup wizard & validator |
| **requirements.txt** | Python dependencies |
| **.env.example** | Environment template |
| **README.md** | Full documentation |

---

## ⚙️ Configuration

Edit these for your trading style:

```python
# In agent.py or .env
SYMBOLS = ['AAPL', 'MSFT', 'TSLA', 'SPY']
CHECK_INTERVAL = 60  # seconds
MAX_DAILY_LOSS = -5000  # USD
RISK_PER_TRADE = 0.02  # 2% of account
```

---

## 🎯 Key Features

✅ **Autonomous Trading**: Runs 24/7 (market hours)
✅ **Options Strategies**: Bull calls, bull puts, spreads  
✅ **Risk Management**: Position sizing, stop losses, profit takes
✅ **Technical Analysis**: RSI, MACD, Bollinger Bands, Trends
✅ **Real-time Monitoring**: Streamlit dashboard
✅ **Trade Logging**: Full audit trail of all trades

---

## 📈 Trading Flow

```
1. Analyze Market (every 60s)
   ↓
2. Generate Signals
   ├─ BUY_CALL (bullish)
   ├─ BUY_PUT (bearish)
   └─ HOLD (neutral)
   ↓
3. Execute Trade (if signal strength > threshold)
   ↓
4. Monitor Position
   ├─ Take profit at +2%
   ├─ Stop loss at -1.5%
   └─ Check daily loss limit
   ↓
5. Log Results & Repeat
```

---

## 🔐 Security Notes

- ⚠️ **NEVER** commit `.env` to git
- ⚠️ Use paper trading keys only
- ⚠️ Test thoroughly before live trading
- ✅ Add to `.gitignore`: `.env`, `*.log`, `trading_log.csv`

---

## 🆘 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API Connection Error"
- Verify `.env` credentials
- Check Alpaca account is active
- Ensure paper trading enabled

### "No Signals Generated"
- Check market hours (9:30 AM - 4:00 PM EST)
- Lower `MIN_CONFIDENCE` in `config.py`
- Verify symbol data is available

### "Dashboard won't load"
```bash
streamlit run dashboard.py --logger.level=debug
```

---

## 📚 Resources

- [Alpaca API Docs](https://alpaca.markets/docs/)
- [Trading API](https://alpaca.markets/docs/api-references/trading-api/)
- [Market Data API](https://alpaca.markets/docs/api-references/market-data-api/)
- [Technical Analysis Indicators](https://ta-lib.org/)

---

## 🏆 Hackathon Requirements

This implementation includes:

- ✅ Autonomous AI trading agent
- ✅ Alpaca Trading API integration
- ✅ Options trading strategies
- ✅ Paper trading ($100K account)
- ✅ Risk management gates
- ✅ Real-time P&L monitoring

---

## 🚨 IMPORTANT DISCLAIMERS

- Past performance does NOT guarantee future results
- Paper trading is simulation only
- No real money is transacted
- Always test thoroughly before live trading
- Trading involves significant risk of loss
- Do NOT use with real capital without extensive testing

---

**Ready to trade?** Run: `python startup.py`

**Monitor trades?** Run: `streamlit run dashboard.py`

Happy trading! 🚀📈

