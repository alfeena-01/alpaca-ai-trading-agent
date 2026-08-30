"""
Advanced Trading Strategies Module
Contains additional strategy implementations for different market conditions.
"""

import pandas as pd
import numpy as np
from ta import momentum, trend, volatility


class AdvancedStrategies:
    """Collection of advanced trading strategies."""
    
    @staticmethod
    def mean_reversion_strategy(bars_df, symbol):
        """
        Mean Reversion Strategy:
        - Buy when price drops below lower Bollinger Band
        - Sell when price rises above upper Bollinger Band
        - Works best in ranging markets
        """
        if len(bars_df) < 20:
            return None
        
        try:
            closes = bars_df['c']
            current_price = closes.iloc[-1]
            
            # Calculate Bollinger Bands
            bb = volatility.BollingerBands(close=closes, window=20, window_dev=2)
            upper_band = bb.bollinger_hband().iloc[-1]
            lower_band = bb.bollinger_lband().iloc[-1]
            middle_band = bb.bollinger_mavg().iloc[-1]
            
            # Signal generation
            if current_price < lower_band:
                strength = (lower_band - current_price) / (upper_band - lower_band)
                return {
                    'signal': 'BUY_CALL',
                    'confidence': min(strength, 1.0),
                    'strategy': 'Mean Reversion',
                    'reason': f'Price {current_price:.2f} below lower band {lower_band:.2f}'
                }
            
            elif current_price > upper_band:
                strength = (current_price - upper_band) / (upper_band - lower_band)
                return {
                    'signal': 'BUY_PUT',
                    'confidence': min(strength, 1.0),
                    'strategy': 'Mean Reversion',
                    'reason': f'Price {current_price:.2f} above upper band {upper_band:.2f}'
                }
            
            return {'signal': 'HOLD', 'strategy': 'Mean Reversion'}
        
        except Exception as e:
            print(f"Error in mean reversion: {e}")
            return None
    
    @staticmethod
    def momentum_strategy(bars_df, symbol):
        """
        Momentum Strategy:
        - Buy when RSI < 30 (oversold) + MACD positive
        - Sell when RSI > 70 (overbought) + MACD negative
        - Follows trend momentum
        """
        if len(bars_df) < 26:
            return None
        
        try:
            closes = bars_df['c']
            current_price = closes.iloc[-1]
            
            # RSI
            rsi = momentum.RSIIndicator(close=closes, window=14).rsi()
            current_rsi = rsi.iloc[-1]
            
            # MACD
            macd = trend.MACD(close=closes, window_fast=12, window_slow=26, window_sign=9)
            macd_diff = macd.macd_diff().iloc[-1]
            
            # Signal generation
            if current_rsi < 30 and macd_diff > 0:
                confidence = (30 - current_rsi) / 30
                return {
                    'signal': 'BUY_CALL',
                    'confidence': min(confidence, 1.0),
                    'strategy': 'Momentum',
                    'reason': f'RSI {current_rsi:.1f} oversold + MACD positive'
                }
            
            elif current_rsi > 70 and macd_diff < 0:
                confidence = (current_rsi - 70) / 30
                return {
                    'signal': 'BUY_PUT',
                    'confidence': min(confidence, 1.0),
                    'strategy': 'Momentum',
                    'reason': f'RSI {current_rsi:.1f} overbought + MACD negative'
                }
            
            return {'signal': 'HOLD', 'strategy': 'Momentum'}
        
        except Exception as e:
            print(f"Error in momentum strategy: {e}")
            return None
    
    @staticmethod
    def trend_following_strategy(bars_df, symbol):
        """
        Trend Following Strategy:
        - Buy when price > SMA50 and SMA50 > SMA200
        - Sell when price < SMA50 or SMA50 < SMA200
        - Follows established trends
        """
        if len(bars_df) < 200:
            return None
        
        try:
            closes = bars_df['c']
            current_price = closes.iloc[-1]
            
            # Moving averages
            sma_20 = closes.rolling(20).mean().iloc[-1]
            sma_50 = closes.rolling(50).mean().iloc[-1]
            sma_200 = closes.rolling(200).mean().iloc[-1]
            
            # Trend strength
            uptrend_strength = 0
            if current_price > sma_20:
                uptrend_strength += 0.25
            if sma_20 > sma_50:
                uptrend_strength += 0.25
            if sma_50 > sma_200:
                uptrend_strength += 0.5
            
            # Signal generation
            if uptrend_strength >= 0.75:
                return {
                    'signal': 'BUY_CALL',
                    'confidence': min(uptrend_strength, 1.0),
                    'strategy': 'Trend Following',
                    'reason': f'Strong uptrend: Price {current_price:.2f} > SMA50 {sma_50:.2f} > SMA200 {sma_200:.2f}'
                }
            
            elif uptrend_strength <= 0.25:
                return {
                    'signal': 'BUY_PUT',
                    'confidence': min(1.0 - uptrend_strength, 1.0),
                    'strategy': 'Trend Following',
                    'reason': 'Price below key moving averages - downtrend'
                }
            
            return {'signal': 'HOLD', 'strategy': 'Trend Following'}
        
        except Exception as e:
            print(f"Error in trend following: {e}")
            return None
    
    @staticmethod
    def volatility_expansion_strategy(bars_df, symbol):
        """
        Volatility Expansion Strategy:
        - Trade when volatility is expanding
        - Buy calls when ATR increasing + RSI not overbought
        - Buy puts when ATR increasing + RSI not oversold
        - Useful for breakout trading
        """
        if len(bars_df) < 14:
            return None
        
        try:
            high = bars_df['h']
            low = bars_df['l']
            close = bars_df['c']
            
            # ATR (Average True Range)
            tr = pd.concat([
                high - low,
                (high - close.shift()).abs(),
                (low - close.shift()).abs()
            ], axis=1).max(axis=1)
            
            atr = tr.rolling(14).mean()
            current_atr = atr.iloc[-1]
            prev_atr = atr.iloc[-2]
            
            # RSI
            rsi = momentum.RSIIndicator(close=close, window=14).rsi()
            current_rsi = rsi.iloc[-1]
            
            # ATR expansion
            atr_expansion = (current_atr - prev_atr) / prev_atr if prev_atr != 0 else 0
            
            # Signal generation
            if atr_expansion > 0.05 and current_rsi < 70:
                return {
                    'signal': 'BUY_CALL',
                    'confidence': min(atr_expansion * 10, 1.0),
                    'strategy': 'Volatility Expansion',
                    'reason': f'ATR expanding {atr_expansion*100:.1f}% + RSI {current_rsi:.1f}'
                }
            
            elif atr_expansion > 0.05 and current_rsi > 30:
                return {
                    'signal': 'BUY_PUT',
                    'confidence': min(atr_expansion * 10, 1.0),
                    'strategy': 'Volatility Expansion',
                    'reason': f'ATR expanding {atr_expansion*100:.1f}% + RSI {current_rsi:.1f}'
                }
            
            return {'signal': 'HOLD', 'strategy': 'Volatility Expansion'}
        
        except Exception as e:
            print(f"Error in volatility expansion: {e}")
            return None
    
    @staticmethod
    def multi_strategy_ensemble(bars_df, symbol):
        """
        Ensemble Strategy:
        - Combines multiple strategies
        - Trades only when multiple strategies agree
        - Reduces false signals
        """
        strategies = [
            AdvancedStrategies.mean_reversion_strategy(bars_df, symbol),
            AdvancedStrategies.momentum_strategy(bars_df, symbol),
            AdvancedStrategies.trend_following_strategy(bars_df, symbol),
        ]
        
        valid_signals = [s for s in strategies if s and s['signal'] != 'HOLD']
        
        if len(valid_signals) == 0:
            return {'signal': 'HOLD', 'strategy': 'Ensemble', 'confidence': 0}
        
        # Count signals
        buy_signals = len([s for s in valid_signals if s['signal'] == 'BUY_CALL'])
        sell_signals = len([s for s in valid_signals if s['signal'] == 'BUY_PUT'])
        
        confidence = max(buy_signals, sell_signals) / len(valid_signals)
        
        if buy_signals > sell_signals:
            return {
                'signal': 'BUY_CALL',
                'confidence': confidence,
                'strategy': 'Ensemble',
                'strategies_agreeing': buy_signals,
                'reason': f'{buy_signals}/{len(valid_signals)} strategies bullish'
            }
        
        elif sell_signals > buy_signals:
            return {
                'signal': 'BUY_PUT',
                'confidence': confidence,
                'strategy': 'Ensemble',
                'strategies_agreeing': sell_signals,
                'reason': f'{sell_signals}/{len(valid_signals)} strategies bearish'
            }
        
        return {'signal': 'HOLD', 'strategy': 'Ensemble', 'confidence': 0.5}


class OptionsStrategies:
    """Specialized options trading strategies."""
    
    @staticmethod
    def iron_condor(current_price, atm_vol, days_to_expiry=30):
        """
        Iron Condor Strategy:
        - Profitable in low volatility environments
        - Limited profit, limited risk
        - 4 legs: Sell put spread + Sell call spread
        """
        # ATM strike
        atm_strike = round(current_price / 5) * 5
        
        # Calculate spread widths
        spread_width = 5
        
        return {
            'strategy': 'IRON_CONDOR',
            'short_put_strike': atm_strike - spread_width,
            'long_put_strike': atm_strike - (spread_width * 2),
            'short_call_strike': atm_strike + spread_width,
            'long_call_strike': atm_strike + (spread_width * 2),
            'max_profit': spread_width * 100 * 2,  # 2 spreads
            'max_loss': spread_width * 100 * 2,    # Width of spreads
            'breakeven_lower': atm_strike - spread_width * 1.5,
            'breakeven_upper': atm_strike + spread_width * 1.5
        }
    
    @staticmethod
    def butterfly_spread(current_price, strike_spacing=5):
        """
        Butterfly Spread Strategy:
        - Limited risk, limited profit
        - Sold for credit typically
        - 3 strikes: 2 wide + 2 middle + 2 wide opposite
        """
        lower_strike = current_price - strike_spacing
        middle_strike = current_price
        upper_strike = current_price + strike_spacing
        
        return {
            'strategy': 'BUTTERFLY_SPREAD',
            'lower_strike': lower_strike,
            'middle_strike': middle_strike,
            'upper_strike': upper_strike,
            'max_profit': strike_spacing * 50,  # Half width
            'max_loss': strike_spacing * 50,    # Half width
            'best_case_expiry': middle_strike
        }
    
    @staticmethod
    def calendar_spread(current_price, front_month_strike, back_month_strike):
        """
        Calendar Spread Strategy:
        - Trade different expiration months
        - Profit from time decay differences
        - Lower risk than directional bets
        """
        return {
            'strategy': 'CALENDAR_SPREAD',
            'front_month_strike': front_month_strike,
            'back_month_strike': back_month_strike,
            'trade_type': 'Long back / Short front',
            'max_profit': 'Unlimited (long side benefits)',
            'risk_profile': 'Limited risk, directional'
        }
