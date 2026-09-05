"""
Utility functions for trading operations, data retrieval, and risk management.
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from alpaca_trade_api import REST
from dotenv import load_dotenv


class AlpacaAPI:
    """Wrapper for Alpaca API interactions."""
    
    def __init__(self):
        """Initialize Alpaca API with environment variables."""
        env_path = Path(__file__).resolve().parent / ".env"
        load_dotenv(dotenv_path=env_path, override=True)
        base_url = os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets").rstrip("/")
        if base_url.endswith("/v2"):
            base_url = base_url[:-3]
        self.api = REST(
            os.getenv("APCA_API_KEY_ID"),
            os.getenv("APCA_API_SECRET_KEY"),
            base_url
        )
    
    def get_account_info(self):
        """Get account information."""
        try:
            account = self.api.get_account()
            return {
                'buying_power': float(account.buying_power),
                'cash': float(account.cash),
                'equity': float(account.equity),
                'multiplier': float(account.multiplier),
                'portfolio_value': float(account.portfolio_value),
                'cash_withdrawable': float(getattr(account, 'cash_withdrawable', account.cash))
            }
        except Exception as e:
            print(f"Error fetching account info: {e}")
            return None
    
    def get_positions(self):
        """Get all open positions."""
        try:
            positions = self.api.list_positions()
            return [{
                'symbol': pos.symbol,
                'qty': float(pos.qty),
                'side': pos.side,
                'entry_price': float(pos.avg_fill_price),
                'current_price': float(pos.current_price),
                'unrealized_pl': float(pos.unrealized_pl),
                'unrealized_plpc': float(pos.unrealized_plpc)
            } for pos in positions]
        except Exception as e:
            print(f"Error fetching positions: {e}")
            return []
    
    def get_bars(self, symbol, timeframe="1Min", limit=100):
        """
        Get historical bars for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            timeframe: Timeframe (1Min, 5Min, 15Min, 1H, 1D)
            limit: Number of bars to retrieve
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            bars = self.api.get_bars(symbol, timeframe, limit=limit)
            if bars is None or len(bars) == 0:
                return None
            
            df = pd.DataFrame({
                't': [bar.t for bar in bars],
                'o': [bar.o for bar in bars],
                'h': [bar.h for bar in bars],
                'l': [bar.l for bar in bars],
                'c': [bar.c for bar in bars],
                'v': [bar.v for bar in bars]
            })
            return df
        except Exception as e:
            print(f"Error fetching bars for {symbol}: {e}")
            return None
    
    def get_latest_quote(self, symbol):
        """Get latest quote for a symbol."""
        try:
            quote = self.api.get_latest_quote(symbol)
            if quote:
                return {
                    'bid': float(quote.bid),
                    'ask': float(quote.ask),
                    'mid': (float(quote.bid) + float(quote.ask)) / 2
                }
        except Exception as e:
            print(f"Error fetching quote for {symbol}: {e}")
        return None
    
    def submit_order(self, symbol, qty, side, order_type="market", time_in_force="gtc", limit_price=None):
        """
        Submit an order.
        
        Args:
            symbol: Stock symbol
            qty: Quantity
            side: 'buy' or 'sell'
            order_type: 'market' or 'limit'
            time_in_force: 'day', 'gtc', 'opg', 'cls'
            limit_price: Price for limit orders
            
        Returns:
            Order object or None
        """
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force=time_in_force,
                limit_price=limit_price
            )
            return {
                'order_id': order.id,
                'symbol': order.symbol,
                'qty': float(order.qty),
                'side': order.side,
                'status': order.status,
                'created_at': order.created_at
            }
        except Exception as e:
            print(f"Error submitting order: {e}")
            return None
    
    def cancel_order(self, order_id):
        """Cancel an order."""
        try:
            self.api.cancel_order(order_id)
            return True
        except Exception as e:
            print(f"Error canceling order: {e}")
            return False
    
    def get_orders(self, status="all"):
        """Get all orders."""
        try:
            orders = self.api.list_orders(status=status)
            return [{
                'order_id': order.id,
                'symbol': order.symbol,
                'qty': float(order.qty),
                'side': order.side,
                'status': order.status,
                'created_at': order.created_at,
                'filled_at': order.filled_at
            } for order in orders]
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []


class RiskManager:
    """Risk management utilities."""
    
    @staticmethod
    def calculate_position_size(account_equity, risk_per_trade, entry_price, stop_loss):
        """
        Calculate optimal position size based on risk.
        
        Args:
            account_equity: Total account equity
            risk_per_trade: Maximum risk per trade (e.g., 0.02 for 2%)
            entry_price: Entry price
            stop_loss: Stop loss price
            
        Returns:
            Number of shares to trade
        """
        risk_amount = account_equity * risk_per_trade
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk == 0:
            return 0
        
        position_size = int(risk_amount / price_risk)
        return max(1, position_size)
    
    @staticmethod
    def calculate_max_loss(position_size, option_premium):
        """Calculate maximum loss for options position."""
        return position_size * option_premium * 100
    
    @staticmethod
    def is_within_risk_limit(current_pl, max_daily_loss):
        """Check if current P&L is within daily loss limit."""
        return current_pl > -max_daily_loss
    
    @staticmethod
    def calculate_stop_loss(entry_price, atr, multiplier=2):
        """Calculate stop loss based on ATR."""
        return entry_price - (atr * multiplier)
    
    @staticmethod
    def calculate_take_profit(entry_price, atr, multiplier=3):
        """Calculate take profit based on ATR."""
        return entry_price + (atr * multiplier)


class DataLogger:
    """Log trading data and statistics."""
    
    def __init__(self, log_file="trading_log.csv"):
        """Initialize logger."""
        self.log_file = log_file
        self.trades = []
    
    def log_trade(self, symbol, signal, qty, price, entry_time):
        """Log a trade execution."""
        trade_data = {
            'timestamp': entry_time,
            'symbol': symbol,
            'signal': signal,
            'qty': qty,
            'price': price
        }
        self.trades.append(trade_data)
        self._save_log()
    
    def log_exit(self, symbol, exit_price, exit_time, pl):
        """Log a trade exit."""
        trade_data = {
            'timestamp': exit_time,
            'symbol': symbol,
            'exit_price': exit_price,
            'pl': pl
        }
        self.trades.append(trade_data)
        self._save_log()
    
    def _save_log(self):
        """Save trades to CSV."""
        try:
            df = pd.DataFrame(self.trades)
            df.to_csv(self.log_file, index=False)
        except Exception as e:
            print(f"Error saving log: {e}")
    
    def get_statistics(self):
        """Calculate trading statistics."""
        if not self.trades:
            return None
        
        df = pd.DataFrame(self.trades)
        return {
            'total_trades': len(df),
            'total_pl': df['pl'].sum() if 'pl' in df.columns else 0,
        }
