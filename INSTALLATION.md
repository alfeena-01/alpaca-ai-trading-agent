# Installation & Troubleshooting Guide

## ✅ Prerequisites Met

- Python 3.10+ installed
- Virtual environment created and activated
- All dependencies installed:
  - ✓ alpaca-trade-api (3.2.0)
  - ✓ python-dotenv
  - ✓ pandas
  - ✓ numpy
  - ✓ plotly
  - ✓ streamlit
  - ✓ requests
  - ✓ pytz, python-dateutil

---

## 🚀 Full Installation Steps

### Step 1: Navigate to Project
```bash
cd c:\Users\User\OneDrive\Desktop\Alpaca
```

### Step 2: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate
```

### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```

If you encounter issues, install packages individually:

```bash
# Core packages
pip install alpaca-trade-api python-dotenv pandas numpy plotly requests pytz python-dateutil

# Streamlit (optional, for dashboard)
pip install streamlit

# Technical analysis (optional)
pip install ta-lib
```

### Step 4: Configure API Credentials

Create `.env` file in project root:
```bash
cp .env.example .env
```

Edit `.env` with your Alpaca credentials:
```env
APCA_API_KEY_ID=your_actual_key
APCA_API_SECRET_KEY=your_actual_secret
APCA_API_BASE_URL=https://paper-api.alpaca.markets
```

### Step 5: Run the Agent
```bash
python agent.py
```

### Step 6: Monitor with Dashboard (Optional)
```bash
# In a new terminal (with venv activated)
streamlit run dashboard.py
```

---

## 🔧 Common Issues & Solutions

### Issue 1: `ModuleNotFoundError: No module named 'plotly'`
**Solution:**
```bash
pip install plotly
```

### Issue 2: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:**
```bash
pip install streamlit
```

### Issue 3: `ModuleNotFoundError: No module named 'ta'`
**Solution:** 
- Install optional ta-lib package:
  ```bash
  pip install ta-lib
  ```
- OR use built-in fallback calculations (code will work without it)

### Issue 4: Websockets Version Conflict
**Solution:**
```bash
pip install 'websockets<11,>=9.0'
```

### Issue 5: `.env file not found`
**Solution:**
```bash
cp .env.example .env
# Then edit .env with your API credentials
```

### Issue 6: API Connection Error
**Solution:**
- Verify API credentials in `.env` are correct
- Ensure Alpaca account is active
- Check paper trading is enabled
- Verify internet connection

### Issue 7: "No Signals Generated"
**Solution:**
- Check market hours (9:30 AM - 4:00 PM EST)
- Lower `MIN_CONFIDENCE_THRESHOLD` in `.env`
- Verify market data is available for the symbol

### Issue 8: Dashboard won't load on `localhost:8501`
**Solution:**
```bash
streamlit run dashboard.py --logger.level=debug
```

---

## 📦 Requirements File Details

**Current versions installed:**

| Package | Version | Purpose |
|---------|---------|---------|
| alpaca-trade-api | 3.2.0 | Alpaca API integration |
| python-dotenv | - | Environment variable management |
| pandas | 2.0+ | Data manipulation |
| numpy | 1.24+ | Numerical computing |
| plotly | 7.0+ | Interactive charts |
| streamlit | <1.30 | Dashboard web framework |
| requests | 2.28+ | HTTP requests |
| python-dateutil | 2.8+ | Date utilities |
| pytz | 2023+ | Timezone handling |

**Note on ta-lib:**
- `ta` (or `ta-lib`) is optional for technical analysis
- Code includes fallback implementations if not installed
- If issues occur, skip ta-lib installation

---

## ✅ Verification Checklist

Run this to verify everything is working:

```bash
# 1. Check Python version
python --version  # Should be 3.10+

# 2. Check virtual environment
which python  # Should show venv path

# 3. Test imports
python -c "import alpaca_trade_api; import pandas; import plotly; import streamlit; print('All imports OK')"

# 4. Test configuration
python -c "from utils import AlpacaAPI; api = AlpacaAPI(); print('API initialized')"

# 5. List installed packages
pip list | findstr alpaca

```

---

## 📋 File Structure After Install

```
Alpaca/
├── venv/                      # Virtual environment
├── agent.py                   # Trading agent (ready ✓)
├── strategy.py                # Strategy module (ready ✓)
├── utils.py                   # Utilities (ready ✓)
├── dashboard.py               # Streamlit dashboard (ready ✓)
├── config.py                  # Configuration (ready ✓)
├── startup.py                 # Setup wizard (ready ✓)
├── advanced_strategies.py     # Advanced strategies (ready ✓)
├── requirements.txt           # Dependencies (updated ✓)
├── .env                       # Your credentials (create this)
├── .env.example               # Template
├── README.md                  # Full documentation
├── QUICKSTART.md              # Quick start
└── INSTALLATION.md            # This file
```

---

## 🎯 Quick Start After Install

### Option A: Interactive Menu
```bash
python startup.py
```
Then select option 1 to start trading

### Option B: Direct Agent
```bash
python agent.py
```

### Option C: Dashboard Only
```bash
streamlit run dashboard.py
```

---

## 🚨 Important Security Notes

1. ⚠️ **NEVER commit `.env` to Git**
   - Add to `.gitignore`: `.env`

2. ⚠️ **Use Paper Trading Only**
   - Make sure Alpaca API URL is: `https://paper-api.alpaca.markets`

3. ⚠️ **Keep Credentials Secure**
   - Don't share `.env` file
   - Use environment-specific credentials

4. ✅ **Test Thoroughly**
   - Test on paper trading first
   - Verify all features work
   - Check risk management settings

---

## 📞 Additional Resources

- [Alpaca API Documentation](https://alpaca.markets/docs/api-references/trading-api/)
- [Python Virtual Environment Guide](https://docs.python.org/3/tutorial/venv.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Graphing](https://plotly.com/python/)

---

## ✨ All Systems Ready

**Status: ✅ READY TO TRADE**

All Python files validated ✓
All dependencies installed ✓
Configuration template created ✓
Documentation complete ✓

**Next Step:** Add your Alpaca credentials to `.env` and run `python agent.py`

---

*Last Updated: 2026-08-30*
*Alpaca AI Trading Agents Hackathon*
