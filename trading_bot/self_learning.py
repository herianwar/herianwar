import pandas as pd
from pathlib import Path
from datetime import datetime
from .model import TradingModel

LOG_FILE = Path('trading_log.csv')


def log_trade(symbol: str, signal: str, profit: float) -> None:
    df = pd.DataFrame([
        {'time': datetime.utcnow(), 'symbol': symbol, 'signal': signal, 'profit': profit}
    ])
    if LOG_FILE.exists():
        df.to_csv(LOG_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)


def load_trades() -> pd.DataFrame:
    if LOG_FILE.exists():
        return pd.read_csv(LOG_FILE)
    return pd.DataFrame(columns=['time', 'symbol', 'signal', 'profit'])


def retrain(model: TradingModel) -> None:
    df = load_trades()
    if df.empty:
        print('No trades to train on.')
        return
    # For simplicity we assume OHLC data is stored as part of trade log for retraining
    # In production you'd reload historical data based on timestamps
    print('Retraining model from log...')
    # Placeholder: not implemented due to limited context
