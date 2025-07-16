import pandas as pd
from datetime import datetime
try:
    import MetaTrader5 as mt5
except ImportError:  # placeholder for environment without MetaTrader5
    mt5 = None


def initialize_mt5():
    if mt5 is None:
        raise RuntimeError("MetaTrader5 package is not installed")
    if not mt5.initialize():
        raise RuntimeError(f"initialize() failed, error code: {mt5.last_error()}")


def shutdown_mt5():
    if mt5:
        mt5.shutdown()


def get_ohlc(symbol: str, timeframe, bars: int = 1000) -> pd.DataFrame:
    """Fetch OHLC data from MT5."""
    if mt5 is None:
        raise RuntimeError("MetaTrader5 package is not installed")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
