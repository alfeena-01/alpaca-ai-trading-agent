"""
Verification script to check all components are working
Run this to ensure everything is installed and configured correctly
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Verify Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} installed")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} too old (need 3.8+)")
        return False


def check_virtual_env():
    """Check if running in virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print(f"✓ Virtual environment active: {sys.prefix}")
        return True
    else:
        print("✗ Not in virtual environment (run: venv\\Scripts\\activate)")
        return False


def check_imports():
    """Check all required packages can be imported."""
    packages = {
        'alpaca_trade_api': 'Alpaca Trading API',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'plotly': 'Plotly',
        'streamlit': 'Streamlit',
        'dotenv': 'Python-DotEnv',
        'requests': 'Requests',
        'pytz': 'PyTZ',
    }
    
    all_ok = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"✗ {name} NOT installed")
            all_ok = False
    
    return all_ok


def check_env_file():
    """Check if .env file exists and is configured."""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("✗ .env file NOT found (copy from .env.example)")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_api_key_here' in content or 'your_secret_key_here' in content:
            print("✗ .env file has placeholder values (configure with real credentials)")
            return False
    
    print("✓ .env file configured")
    return True


def check_python_files():
    """Check all Python files are syntactically correct."""
    files = [
        'agent.py',
        'strategy.py',
        'utils.py',
        'config.py',
        'startup.py',
        'advanced_strategies.py',
        'dashboard.py',
    ]
    
    all_ok = True
    for file in files:
        try:
            compile(open(file).read(), file, 'exec')
            print(f"✓ {file} syntax OK")
        except SyntaxError as e:
            print(f"✗ {file} has syntax errors: {e}")
            all_ok = False
    
    return all_ok


def check_api_connection():
    """Test connection to Alpaca API."""
    try:
        from utils import AlpacaAPI
        api = AlpacaAPI()
        account = api.get_account_info()
        
        if account:
            print(f"✓ Alpaca API connected")
            print(f"  - Account equity: ${account['equity']:,.2f}")
            print(f"  - Buying power: ${account['buying_power']:,.2f}")
            return True
        else:
            print("✗ Could not fetch account information")
            return False
    except Exception as e:
        print(f"✗ API connection failed: {e}")
        return False


def check_strategy():
    """Test strategy module."""
    try:
        from strategy import TradingStrategy
        strategy = TradingStrategy()
        print("✓ Trading strategy module loads")
        return True
    except Exception as e:
        print(f"✗ Strategy module error: {e}")
        return False


def run_diagnostics():
    """Run all diagnostics."""
    print("\n" + "="*60)
    print("ALPACA TRADING AGENT - SYSTEM DIAGNOSTICS")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_env),
        ("Package Imports", check_imports),
        ("Configuration (.env)", check_env_file),
        ("Python Files", check_python_files),
        ("Strategy Module", check_strategy),
        ("Alpaca API Connection", check_api_connection),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 40)
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"✗ Error during check: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {check_name}")
    
    print("\n" + "="*60)
    if passed == total:
        print("✓ ALL CHECKS PASSED - READY TO TRADE!")
        print("\nRun: python agent.py")
    else:
        print(f"✗ {total - passed} checks failed - see above for details")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_diagnostics()
    sys.exit(0 if success else 1)
