"""
Real-time Trading Dashboard for Alpaca Trading Agent.
Displays live P&L, positions, trading history, and market analysis.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from utils import AlpacaAPI, DataLogger
from strategy import TradingStrategy

# Page configuration
st.set_page_config(
    page_title="Alpaca Trading Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .positive { color: #26a65b; }
    .negative { color: #e74c3c; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api' not in st.session_state:
    st.session_state.api = AlpacaAPI()
if 'strategy' not in st.session_state:
    st.session_state.strategy = TradingStrategy()
if 'refresh_count' not in st.session_state:
    st.session_state.refresh_count = 0

# Sidebar
st.sidebar.title("⚙️ Settings")
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 300, 30)
selected_symbols = st.sidebar.multiselect(
    "Symbols to Monitor",
    ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMD', 'AMZN', 'SPY', 'QQQ', 'IWM'],
    default=['AAPL', 'MSFT', 'TSLA', 'SPY']
)

# Main title
st.title("📊 Alpaca AI Trading Agent Dashboard")
st.markdown("Real-time autonomous trading monitoring and analysis")

# Account Overview
st.header("Account Overview")
col1, col2, col3, col4 = st.columns(4)

try:
    account = st.session_state.api.get_account_info()
    
    if account:
        with col1:
            st.metric("Portfolio Value", f"${account['equity']:,.2f}", delta=None)
        
        with col2:
            st.metric("Cash Available", f"${account['cash']:,.2f}")
        
        with col3:
            st.metric("Buying Power", f"${account['buying_power']:,.2f}")
        
        with col4:
            multiplier = account['multiplier']
            st.metric("Leverage", f"{multiplier}x")
    
    else:
        st.error("Unable to fetch account information. Check API credentials.")

except Exception as e:
    st.error(f"Error loading account data: {e}")

# Positions Section
st.header("📍 Open Positions")
try:
    positions = st.session_state.api.get_positions()
    
    if positions:
        positions_df = pd.DataFrame(positions)
        positions_df['PL %'] = positions_df['unrealized_plpc'] * 100
        positions_df['Unrealized P&L'] = positions_df['unrealized_pl']
        
        # Display positions table
        display_cols = ['symbol', 'qty', 'side', 'entry_price', 'current_price', 'Unrealized P&L', 'PL %']
        positions_display = positions_df[display_cols].copy()
        positions_display.columns = ['Symbol', 'Qty', 'Side', 'Entry Price', 'Current Price', 'P&L', 'P&L %']
        
        st.dataframe(
            positions_display,
            use_container_width=True,
            height=200
        )
        
        # P&L Summary
        total_pl = positions_df['Unrealized P&L'].sum()
        total_pl_pct = (total_pl / account['equity'] * 100) if account else 0
        
        col1, col2 = st.columns(2)
        with col1:
            if total_pl >= 0:
                st.metric("Total Unrealized P&L", f"${total_pl:,.2f}", 
                         delta=f"{total_pl_pct:.2f}%", delta_color="normal")
            else:
                st.metric("Total Unrealized P&L", f"${total_pl:,.2f}", 
                         delta=f"{total_pl_pct:.2f}%", delta_color="inverse")
        
        with col2:
            st.metric("Number of Positions", len(positions))
    else:
        st.info("No open positions")

except Exception as e:
    st.warning(f"Could not load positions: {e}")

# Market Analysis Section
st.header("📈 Market Analysis")
analysis_col1, analysis_col2 = st.columns([2, 1])

with analysis_col1:
    if selected_symbols:
        st.subheader("Price Action Analysis")
        
        analysis_data = []
        
        for symbol in selected_symbols:
            try:
                bars = st.session_state.api.get_bars(symbol, timeframe="5Min", limit=100)
                
                if bars is not None and len(bars) > 0:
                    signal = st.session_state.strategy.generate_signal(bars, symbol, account['equity'] if account else 100000)
                    
                    if signal:
                        current_price = bars['c'].iloc[-1]
                        analysis_data.append({
                            'Symbol': symbol,
                            'Price': f"${current_price:.2f}",
                            'Signal': signal['signal'],
                            'Confidence': f"{signal['confidence']*100:.1f}%",
                            'Trend Score': f"{signal['trend_score']:.2f}"
                        })
            
            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")
        
        if analysis_data:
            analysis_df = pd.DataFrame(analysis_data)
            st.dataframe(analysis_df, use_container_width=True, hide_index=True, height=300)
        else:
            st.info("No analysis available")
    else:
        st.info("Select symbols in the sidebar to analyze")

with analysis_col2:
    st.subheader("Signal Distribution")
    if selected_symbols and analysis_data:
        signal_counts = pd.Series([d['Signal'] for d in analysis_data]).value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=signal_counts.index,
            values=signal_counts.values,
            hole=.3
        )])
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

# Recent Orders
st.header("📋 Recent Orders")
try:
    orders = st.session_state.api.get_orders(status='all')
    
    if orders:
        orders_df = pd.DataFrame(orders)
        # Show last 10 orders
        orders_df = orders_df.head(10)
        
        display_cols = ['symbol', 'qty', 'side', 'status', 'created_at']
        orders_display = orders_df[display_cols].copy()
        orders_display.columns = ['Symbol', 'Qty', 'Side', 'Status', 'Created']
        
        st.dataframe(orders_display, use_container_width=True, height=200, hide_index=True)
    else:
        st.info("No orders found")

except Exception as e:
    st.warning(f"Could not load orders: {e}")

# Risk Metrics
st.header("⚠️ Risk Metrics")
col1, col2, col3 = st.columns(3)

try:
    with col1:
        st.metric("Max Daily Loss Limit", "$5,000")
    
    with col2:
        if positions:
            largest_pos = max(positions, key=lambda x: abs(x['unrealized_pl']))
            st.metric("Largest Position Loss", f"${largest_pos['unrealized_pl']:.2f}")
        else:
            st.metric("Largest Position Loss", "$0.00")
    
    with col3:
        if account:
            risk_pct = (account['cash'] / account['equity'] * 100) if account['equity'] > 0 else 0
            st.metric("Cash as % of Portfolio", f"{risk_pct:.1f}%")
        else:
            st.metric("Cash as % of Portfolio", "N/A")

except Exception as e:
    st.warning(f"Could not calculate risk metrics: {e}")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.8em;'>
    Alpaca AI Trading Agents Hackathon | 
    Last Updated: {0} | 
    Status: Running
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
