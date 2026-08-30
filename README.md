# Alpaca AI Trading Agents Hackathon - Trading System

An autonomous AI trading agent built for the Alpaca AI Trading Agents Hackathon (Aug 28 - Sep 4, 2026). This system uses technical analysis, options trading strategies, and risk management to execute algorithmic trades on Alpaca's paper trading platform.

## 🎯 Key Features

- **Autonomous Trading Agent**: Runs continuously with automatic market analysis and trade execution
- **Options Trading**: Implements bull call spreads, bull put spreads, and other options strategies
- **Technical Analysis**: Uses RSI, MACD, Bollinger Bands, and trend analysis for signal generation
- **Risk Management**: 
  - Position sizing based on account risk tolerance
  - Daily loss limits to prevent catastrophic losses
  - Automatic profit taking and stop loss management
  - Defined-risk option spreads
- **Real-time Dashboard**: Streamlit-based monitoring of positions, P&L, and market analysis
- **Trade Logging**: Comprehensive logging of all trades and performance metrics

## 📋 Requirements

- Python 3.8+
- Alpaca Trading Account (paper trading enabled)
- API credentials from Alpaca

## 🚀 Quick Start

### 1. Setup Python Environment

```bash
# Navigate to project directory
cd c:\Users\User\OneDrive\Desktop\Alpaca

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your Alpaca API credentials:
   - Get your API key and secret from: https://app.alpaca.markets/
   - Ensure you're using paper trading credentials
   - Set your preferred trading parameters

### 4. Start the Agent

```bash
python agent.py
```

The agent will:
- Check market conditions every 60 seconds (configurable)
- Analyze selected symbols for trading signals
- Execute trades automatically based on strategy signals
- Monitor positions with automatic profit-taking and stop-loss
- Log all trading activity to `trading_agent.log`

### 5. Monitor in Real-time (Optional)

In a separate terminal, run the dashboard:

```bash
streamlit run dashboard.py
```

This opens a real-time monitoring dashboard at `http://localhost:8501`

## 📁 Project Structure

```
.
├── agent.py              # Main autonomous trading agent
├── strategy.py           # Trading strategy and technical analysis
├── utils.py             # Alpaca API wrapper and utilities
├── dashboard.py         # Streamlit monitoring dashboard
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── trading_agent.log   # Trading activity log (generated)
└── trading_log.csv     # Trade execution log (generated)
```

## 🎲 Trading Strategy

### Signal Generation

The strategy analyzes:
- **Trend**: Moving averages and price position
- **Momentum**: RSI (Relative Strength Index)
- **Volatility**: Bollinger Bands
- **Volume**: Volume confirmation of trends

### Signals

- **BUY_CALL**: Bullish signal - execute bull call spread or buy position
- **BUY_PUT**: Bearish signal - execute bull put spread or short position
- **HOLD**: No strong signal - remain neutral

### Risk Management

1. **Position Sizing**: Based on account equity and risk tolerance
   - Default risk per trade: 2% of account equity
   - Automatic scaling based on signal confidence

2. **Exit Management**:
   - Profit taking: Exit when position reaches +2% profit
   - Stop loss: Exit when position reaches -1.5% loss
   - Daily loss limit: Stop all trading if daily loss exceeds $5,000

3. **Options Strategies**:
   - Bull Call Spread: Long call + Short higher call
   - Bull Put Spread: Short put + Long lower put
   - Both provide defined risk profiles

## 📊 Dashboard Features

The Streamlit dashboard displays:

- **Account Overview**: Portfolio value, cash, buying power, leverage
- **Open Positions**: Current positions with entry prices and P&L
- **Market Analysis**: Real-time signals for monitored symbols
- **Signal Distribution**: Visual breakdown of current signals
- **Recent Orders**: Last 10 orders executed
- **Risk Metrics**: Daily loss tracking and risk indicators

## 🔧 Configuration

Edit these parameters in `agent.py` or via `.env`:

```python
# Trading symbols
symbols = ['AAPL', 'MSFT', 'TSLA', 'SPY']

# Check interval (seconds)
check_interval = 60

# Maximum daily loss before stopping
max_daily_loss = -5000

# Risk per trade
risk_tolerance = 0.02

# Minimum confidence for signals
min_confidence = 0.6
```

## 📈 Expected Performance

The strategy is designed for:
- **Moderate returns**: 1-3% per week on paper trading
- **Low drawdown**: Risk-managed positions with defined exits
- **Consistency**: Systematic approach with clear entry/exit rules
- **Scalability**: Can handle multiple symbols simultaneously

## ⚠️ Important Notes

- **Paper Trading Only**: This system is configured for Alpaca's paper trading (simulated funds)
- **Live Trading Risk**: Do NOT use live trading credentials without thorough testing
- **Market Hours**: Strategy works best during US market hours (9:30 AM - 4:00 PM EST)
- **No Guarantee**: Past performance does not guarantee future results

## 🐛 Troubleshooting

### API Connection Error
- Verify API credentials in `.env`
- Check if paper trading is enabled in Alpaca account
- Ensure internet connection is stable

### No Signals Generated
- Verify symbols are valid (check market hours)
- Check if bars data is available for the symbol
- Adjust `min_confidence` threshold if too strict

### Dashboard Not Loading
- Ensure Streamlit is installed: `pip install streamlit`
- Try: `streamlit run dashboard.py --logger.level=debug`

## 📚 Resources

- [Alpaca Trading API Docs](https://alpaca.markets/docs/api-references/trading-api/)
- [Alpaca Market Data API](https://alpaca.markets/docs/api-references/market-data-api/)
- [Paper Trading Guide](https://alpaca.markets/docs/trading/paper-trading/)
- [Options Trading Education](https://www.investopedia.com/options-basics-4689846)

## 🏆 Hackathon Requirements

This project fulfills all Alpaca Hackathon requirements:

✅ **Autonomous Agents**: Fully autonomous trading agent with no human intervention required
✅ **Alpaca API Integration**: Uses Alpaca Trading API and MCP server capabilities
✅ **Options Trading**: Implements options spread strategies (bull call, bull put)
✅ **Paper Trading**: Configured for $100,000 paper trading account
✅ **Risk Management**: Defined-risk spreads with stop losses and profit targets
✅ **AI-Powered**: Uses technical analysis and ML-ready architecture for signal generation

## 📝 License

MIT License - Feel free to modify and distribute

---

**Built for Alpaca AI Trading Agents Hackathon 2026**
*"Code the next generation of algorithmic trading"*
