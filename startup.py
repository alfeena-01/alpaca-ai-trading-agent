"""
Startup script for Alpaca Trading Agent.
Handles initialization, validation, and starting the agent.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_requirements():
    """Check if all required packages are installed."""
    required_packages = [
        'dotenv',
        'alpaca_trade_api',
        'pandas',
        'numpy',
        'ta',
        'streamlit',
        'plotly'
    ]
    
    logger.info("Checking requirements...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package if package != 'alpaca_trade_api' else 'alpaca.trading')
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Run: pip install -r requirements.txt")
        return False
    
    logger.info("✓ All requirements installed")
    return True


def check_env_file():
    """Check if .env file exists and is configured."""
    env_file = Path('.env')
    
    if not env_file.exists():
        logger.error(".env file not found!")
        logger.info("1. Copy .env.example to .env")
        logger.info("2. Fill in your Alpaca API credentials")
        logger.info("3. Run this script again")
        return False
    
    # Check if credentials are set
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_api_key_here' in content or 'your_secret_key_here' in content:
            logger.error(".env file contains placeholder values!")
            logger.info("Please configure your Alpaca API credentials in .env")
            return False
    
    logger.info("✓ .env file configured")
    return True


def validate_alpaca_connection():
    """Validate connection to Alpaca API."""
    try:
        logger.info("Validating Alpaca connection...")
        
        from utils import AlpacaAPI
        api = AlpacaAPI()
        account = api.get_account_info()
        
        if account:
            logger.info(f"✓ Connected to Alpaca")
            logger.info(f"  Account Equity: ${account['equity']:,.2f}")
            logger.info(f"  Buying Power: ${account['buying_power']:,.2f}")
            logger.info(f"  Cash: ${account['cash']:,.2f}")
            return True
        else:
            logger.error("Could not fetch account information")
            return False
    
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return False


def show_startup_menu():
    """Show startup menu with options."""
    print("\n" + "="*60)
    print("ALPACA AI TRADING AGENT - STARTUP MENU")
    print("="*60)
    print("\nSelect an option:")
    print("1. Start Trading Agent")
    print("2. Run Dashboard Only")
    print("3. Validate Configuration")
    print("4. Check API Connection")
    print("5. Exit")
    print("\n" + "="*60)
    
    choice = input("\nEnter your choice (1-5): ").strip()
    return choice


def start_agent():
    """Start the trading agent."""
    logger.info("Starting Trading Agent...")
    print("\n" + "="*60)
    print("ALPACA AUTONOMOUS TRADING AGENT")
    print("="*60)
    
    try:
        from agent import AutonomousTradingAgent
        
        agent = AutonomousTradingAgent(
            symbols=['AAPL', 'MSFT', 'TSLA', 'SPY'],
            check_interval=60,
            max_daily_loss=-5000
        )
        
        agent.run()
    
    except KeyboardInterrupt:
        logger.info("\nAgent interrupted by user")
    except Exception as e:
        logger.error(f"Error starting agent: {e}")
        sys.exit(1)


def start_dashboard():
    """Start the Streamlit dashboard."""
    logger.info("Starting Dashboard...")
    os.system("streamlit run dashboard.py")


def validate_configuration():
    """Validate all configuration."""
    print("\n" + "="*60)
    print("CONFIGURATION VALIDATION")
    print("="*60)
    
    checks = {
        "Requirements": check_requirements,
        ".env File": check_env_file,
        "Alpaca Connection": validate_alpaca_connection
    }
    
    all_passed = True
    for check_name, check_func in checks.items():
        print(f"\nChecking {check_name}...")
        if check_func():
            print(f"  ✓ {check_name} OK")
        else:
            print(f"  ✗ {check_name} FAILED")
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ All checks passed! Ready to trade.")
    else:
        print("✗ Some checks failed. Please resolve issues above.")
    print("="*60 + "\n")
    
    return all_passed


def main():
    """Main startup function."""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Show banner
    print("\n" + "="*60)
    print("ALPACA AI TRADING AGENTS HACKATHON")
    print("Autonomous Options Trading System")
    print("="*60 + "\n")
    
    # Initial validation
    logger.info("Performing initial validation...")
    if not check_requirements():
        sys.exit(1)
    
    if not check_env_file():
        sys.exit(1)
    
    logger.info("✓ Initial validation passed\n")
    
    # Main loop
    while True:
        choice = show_startup_menu()
        
        if choice == '1':
            if validate_alpaca_connection():
                start_agent()
            else:
                logger.error("Cannot start agent: Alpaca connection failed")
        
        elif choice == '2':
            start_dashboard()
        
        elif choice == '3':
            validate_configuration()
        
        elif choice == '4':
            validate_alpaca_connection()
        
        elif choice == '5':
            logger.info("Exiting...")
            sys.exit(0)
        
        else:
            logger.warning("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutdown by user")
        sys.exit(0)
