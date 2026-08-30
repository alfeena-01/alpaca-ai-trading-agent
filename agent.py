"""
Autonomous AI Trading Agent for Alpaca.
Executes options and stock trading strategies with risk management.
"""

import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from strategy import TradingStrategy
from utils import AlpacaAPI, RiskManager, DataLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()


class AutonomousTradingAgent:
    """Main autonomous trading agent."""
    
    def __init__(self, symbols=None, check_interval=60, max_daily_loss=-5000):
        """
        Initialize the trading agent.
        
        Args:
            symbols: List of symbols to trade (default: popular stocks)
            check_interval: Seconds between market checks
            max_daily_loss: Maximum allowed daily loss before stopping
        """
        self.symbols = symbols or ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'SPY']
        self.check_interval = check_interval
        self.max_daily_loss = max_daily_loss
        self.api = AlpacaAPI()
        self.strategy = TradingStrategy(risk_tolerance=0.02, min_confidence=0.6)
        self.logger = DataLogger()
        self.active_positions = {}
        self.daily_pl = 0
        self.is_running = False
    
    def get_account_status(self):
        """Get current account status."""
        account = self.api.get_account_info()
        if account:
            logger.info(f"Account Status - Equity: ${account['equity']:.2f}, "
                       f"Buying Power: ${account['buying_power']:.2f}, "
                       f"Cash: ${account['cash']:.2f}")
            return account
        return None
    
    def analyze_market(self):
        """Analyze market for all symbols."""
        signals = {}
        account = self.get_account_status()
        
        if not account:
            return signals
        
        for symbol in self.symbols:
            try:
                # Get bars data
                bars = self.api.get_bars(symbol, timeframe="5Min", limit=100)
                
                if bars is None:
                    logger.warning(f"No bars data for {symbol}")
                    continue
                
                # Generate signal
                signal = self.strategy.generate_signal(
                    bars,
                    symbol,
                    account_equity=account['equity']
                )
                
                if signal and signal['signal'] != 'HOLD':
                    signals[symbol] = signal
                    logger.info(f"{symbol}: {signal['signal']} "
                               f"(confidence: {signal['confidence']:.2f})")
            
            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {e}")
        
        return signals
    
    def execute_trade(self, signal):
        """
        Execute a trade based on signal.
        
        Args:
            signal: Trading signal dictionary
        """
        symbol = signal['symbol']
        position_size = signal['position_size']
        
        if position_size <= 0:
            return None
        
        try:
            quote = self.api.get_latest_quote(symbol)
            if not quote:
                logger.warning(f"Could not get quote for {symbol}")
                return None
            
            entry_price = quote['mid']
            
            # Execute order based on signal
            if signal['signal'] == 'BUY_CALL':
                # Bullish: Buy call option (represented by buying stock)
                order = self.api.submit_order(
                    symbol=symbol,
                    qty=position_size,
                    side='buy',
                    order_type='market'
                )
                logger.info(f"CALL Order: {symbol} x{position_size} @ ${entry_price:.2f}")
            
            elif signal['signal'] == 'BUY_PUT':
                # Bearish: Buy put option (represented by shorting stock)
                order = self.api.submit_order(
                    symbol=symbol,
                    qty=position_size,
                    side='sell',
                    order_type='market'
                )
                logger.info(f"PUT Order: {symbol} x{position_size} @ ${entry_price:.2f}")
            
            if order:
                # Log trade
                self.logger.log_trade(
                    symbol=symbol,
                    signal=signal['signal'],
                    qty=position_size,
                    price=entry_price,
                    entry_time=datetime.now()
                )
                
                # Track position
                self.active_positions[symbol] = {
                    'signal': signal['signal'],
                    'entry_price': entry_price,
                    'qty': position_size,
                    'entry_time': datetime.now()
                }
                
                return order
        
        except Exception as e:
            logger.error(f"Error executing trade for {signal['symbol']}: {e}")
        
        return None
    
    def check_exits(self):
        """Check for exit conditions on open positions."""
        positions = self.api.get_positions()
        
        for position in positions:
            symbol = position['symbol']
            
            # Take profit at 2%
            if position['unrealized_plpc'] > 0.02:
                logger.info(f"Taking profit on {symbol}: {position['unrealized_plpc']*100:.2f}%")
                self.api.submit_order(symbol, position['qty'], 'sell')
                if symbol in self.active_positions:
                    del self.active_positions[symbol]
            
            # Stop loss at -1.5%
            elif position['unrealized_plpc'] < -0.015:
                logger.info(f"Stopping loss on {symbol}: {position['unrealized_plpc']*100:.2f}%")
                self.api.submit_order(symbol, position['qty'], 'sell')
                if symbol in self.active_positions:
                    del self.active_positions[symbol]
    
    def calculate_daily_pl(self):
        """Calculate daily profit/loss."""
        positions = self.api.get_positions()
        self.daily_pl = sum(float(pos['unrealized_pl']) for pos in positions)
        return self.daily_pl
    
    def should_continue_trading(self):
        """Check if agent should continue trading."""
        daily_pl = self.calculate_daily_pl()
        
        if daily_pl < self.max_daily_loss:
            logger.warning(f"Daily loss limit reached: ${daily_pl:.2f}")
            return False
        
        return True
    
    def run(self):
        """Main trading loop."""
        logger.info("=" * 60)
        logger.info("AUTONOMOUS TRADING AGENT STARTED")
        logger.info("=" * 60)
        
        self.is_running = True
        iteration = 0
        
        try:
            while self.is_running:
                iteration += 1
                logger.info(f"\n--- Market Check #{iteration} ---")
                
                # Check if we should continue
                if not self.should_continue_trading():
                    logger.info("Stopping agent: daily loss limit reached")
                    break
                
                # Analyze market
                signals = self.analyze_market()
                
                # Execute trades on new signals
                for symbol, signal in signals.items():
                    if symbol not in self.active_positions:
                        self.execute_trade(signal)
                
                # Check for exits
                self.check_exits()
                
                # Calculate and log daily P&L
                daily_pl = self.calculate_daily_pl()
                logger.info(f"Daily P&L: ${daily_pl:.2f}")
                
                # Wait for next check
                logger.info(f"Waiting {self.check_interval}s for next check...")
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            logger.info("Agent interrupted by user")
        except Exception as e:
            logger.error(f"Fatal error in agent loop: {e}", exc_info=True)
        finally:
            self._shutdown()
    
    def _shutdown(self):
        """Graceful shutdown."""
        logger.info("\nShutting down agent...")
        self.is_running = False
        
        # Log final statistics
        account = self.get_account_status()
        if account:
            logger.info(f"Final Equity: ${account['equity']:.2f}")
            logger.info(f"Final Cash: ${account['cash']:.2f}")
        
        logger.info("Agent shutdown complete")


def main():
    """Main entry point."""
    agent = AutonomousTradingAgent(
        symbols=['AAPL', 'MSFT', 'TSLA', 'SPY'],
        check_interval=60,  # Check every minute
        max_daily_loss=-5000  # Stop if daily loss exceeds $5000
    )
    agent.run()


if __name__ == "__main__":
    main()
