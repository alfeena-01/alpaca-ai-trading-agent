"""
Trading strategy module for options and stock trading.
Incorporates technical analysis and risk management.
"""

import pandas as pd
import numpy as np
try:
    from ta import momentum, trend, volatility
except ImportError:
    # Fallback if ta-lib not available - use built-in calculations
    momentum = trend = volatility = None
from datetime import datetime, timedelta


class TradingStrategy:
    """Options and stock trading strategy with technical analysis."""
    
    def __init__(self, risk_tolerance=0.02, min_confidence=0.6):
        """
        Initialize strategy parameters.
        
        Args:
            risk_tolerance: Maximum risk per trade (default 2%)
            min_confidence: Minimum confidence threshold for signals (0-1)
        """
        self.risk_tolerance = risk_tolerance
        self.min_confidence = min_confidence
        self.current_signals = {}
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index."""
        try:
            if momentum is not None:
                rsi = momentum.RSIIndicator(close=prices, window=period).rsi()
                return rsi.iloc[-1] if len(rsi) > 0 else None
            else:
                # Fallback calculation
                deltas = prices.diff()
                seed = deltas[:period+1]
                up = seed[seed >= 0].sum() / period
                down = -seed[seed < 0].sum() / period
                rs = up / down if down != 0 else 0
                rsi = 100. - 100. / (1. + rs)
                return rsi
        except:
            return None
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator."""
        try:
            if trend is not None:
                macd = trend.MACD(close=prices, window_fast=fast, window_slow=slow, window_sign=signal)
                return {
                    'macd': macd.macd().iloc[-1],
                    'signal': macd.macd_signal().iloc[-1],
                    'histogram': macd.macd_diff().iloc[-1]
                }
            else:
                # Fallback calculation
                ema_fast = prices.ewm(span=fast).mean().iloc[-1]
                ema_slow = prices.ewm(span=slow).mean().iloc[-1]
                macd_val = ema_fast - ema_slow
                return {
                    'macd': macd_val,
                    'signal': macd_val,  # Simplified
                    'histogram': 0
                }
        except:
            return None
    
    def calculate_bollinger_bands(self, prices, period=20, num_std=2):
        """Calculate Bollinger Bands."""
        try:
            if volatility is not None:
                bb = volatility.BollingerBands(close=prices, window=period, window_dev=num_std)
                return {
                    'upper': bb.bollinger_hband().iloc[-1],
                    'middle': bb.bollinger_mavg().iloc[-1],
                    'lower': bb.bollinger_lband().iloc[-1]
                }
            else:
                # Fallback calculation
                middle = prices.rolling(window=period).mean().iloc[-1]
                std = prices.rolling(window=period).std().iloc[-1]
                return {
                    'upper': middle + (std * num_std),
                    'middle': middle,
                    'lower': middle - (std * num_std)
                }
        except:
            return None
    
    def analyze_price_action(self, bars_df):
        """
        Analyze price action from bars data.
        
        Returns: score from -1 (bearish) to 1 (bullish)
        """
        if len(bars_df) < 5:
            return 0
        
        try:
            closes = bars_df['c']
            volumes = bars_df['v']
            
            # Trend analysis
            sma_5 = closes.rolling(5).mean().iloc[-1]
            sma_20 = closes.rolling(20).mean().iloc[-1] if len(closes) >= 20 else sma_5
            current_price = closes.iloc[-1]
            
            trend_score = 0
            if current_price > sma_5:
                trend_score += 0.3
            if sma_5 > sma_20:
                trend_score += 0.2
            
            # RSI analysis
            rsi = self.calculate_rsi(closes, period=14)
            if rsi is not None:
                if rsi < 30:
                    trend_score += 0.25  # Oversold
                elif rsi > 70:
                    trend_score -= 0.25  # Overbought
                else:
                    trend_score += (rsi - 50) / 100  # Scale between -0.5 and 0.5
            
            # Volume analysis
            avg_volume = volumes.rolling(5).mean().iloc[-1]
            current_volume = volumes.iloc[-1]
            if current_volume > avg_volume * 1.2:
                trend_score += 0.15  # Higher volume confirms trend
            
            return np.clip(trend_score, -1, 1)
        
        except Exception as e:
            print(f"Error in price action analysis: {e}")
            return 0
    
    def generate_signal(self, bars_df, symbol, account_equity=100000):
        """
        Generate trading signal for options or stock trading.
        
        Args:
            bars_df: DataFrame with OHLCV data
            symbol: Stock symbol
            account_equity: Current account equity
            
        Returns:
            dict with signal details or None
        """
        if bars_df is None or len(bars_df) < 5:
            return None
        
        try:
            trend_score = self.analyze_price_action(bars_df)
            
            # Generate signal based on trend score
            if trend_score > self.min_confidence:
                confidence = min(trend_score, 1.0)
                return {
                    'symbol': symbol,
                    'signal': 'BUY_CALL',  # Bullish signal
                    'confidence': confidence,
                    'trend_score': trend_score,
                    'timestamp': datetime.now(),
                    'position_size': self._calculate_position_size(confidence, account_equity)
                }
            
            elif trend_score < -self.min_confidence:
                confidence = min(abs(trend_score), 1.0)
                return {
                    'symbol': symbol,
                    'signal': 'BUY_PUT',  # Bearish signal
                    'confidence': confidence,
                    'trend_score': trend_score,
                    'timestamp': datetime.now(),
                    'position_size': self._calculate_position_size(confidence, account_equity)
                }
            
            else:
                return {
                    'symbol': symbol,
                    'signal': 'HOLD',
                    'confidence': 0,
                    'trend_score': trend_score,
                    'timestamp': datetime.now(),
                    'position_size': 0
                }
        
        except Exception as e:
            print(f"Error generating signal for {symbol}: {e}")
            return None
    
    def _calculate_position_size(self, confidence, account_equity):
        """Calculate position size based on confidence and risk tolerance."""
        risk_amount = account_equity * self.risk_tolerance
        position_size = max(1, int((confidence * risk_amount) / 1000))  # Assuming avg option price ~$1000
        return position_size
    
    def generate_bull_call_spread(self, current_price, strike_distance=5):
        """
        Generate bull call spread parameters.
        Buy OTM call, sell higher OTM call.
        """
        long_call_strike = round(current_price + strike_distance, 0)
        short_call_strike = round(current_price + strike_distance * 2, 0)
        
        return {
            'strategy': 'BULL_CALL_SPREAD',
            'long_call_strike': long_call_strike,
            'short_call_strike': short_call_strike,
            'max_profit': (short_call_strike - long_call_strike) * 100,
            'max_loss_is_defined': True
        }
    
    def generate_bull_put_spread(self, current_price, strike_distance=5):
        """
        Generate bull put spread parameters.
        Sell OTM put, buy lower OTM put.
        """
        short_put_strike = round(current_price - strike_distance, 0)
        long_put_strike = round(current_price - strike_distance * 2, 0)
        
        return {
            'strategy': 'BULL_PUT_SPREAD',
            'short_put_strike': short_put_strike,
            'long_put_strike': long_put_strike,
            'max_profit_is_limited': True
        }
