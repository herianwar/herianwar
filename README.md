# AI Trading Bot for MT5

This project provides a basic framework for an automated trading system on MetaTrader 5 (MT5) using machine learning.

## Components

- **`trading_bot/data.py`** – utilities to connect to MT5 and download OHLC data.
- **`trading_bot/model.py`** – defines the `TradingModel` built on top of XGBoost with simple technical features.
- **`trading_bot/trader.py`** – example trader that trains the model and places orders on MT5.
- **`trading_bot/self_learning.py`** – utilities to log trade results and (placeholder) retrain from logs.
- **`trading_bot/ui.py`** – a minimal Streamlit dashboard to display trading logs.

## Usage

1. Install dependencies (MetaTrader5, pandas, scikit-learn, xgboost, streamlit).
2. Initialize connection to MT5 using `data.initialize_mt5()`.
3. Create a `Trader` instance, call `train()` with historical data, then `run_once()` periodically to trade.
4. Use `self_learning.log_trade()` to record trade outcomes and periodically retrain the model.
5. Run `python -m trading_bot.ui` to start the monitoring dashboard.

This is a simplified example – production usage would require extensive testing, error handling and risk management.
