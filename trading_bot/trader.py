from __future__ import annotations
import pandas as pd
from typing import Optional

try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None

from .model import TradingModel
from .data import get_ohlc


class Trader:
    def __init__(self, symbol: str, timeframe=mt5.TIMEFRAME_M5):
        if mt5 is None:
            raise RuntimeError("MetaTrader5 package is not installed")
        self.symbol = symbol
        self.timeframe = timeframe
        self.model = TradingModel()

    def train(self, bars: int = 1000):
        df = get_ohlc(self.symbol, self.timeframe, bars)
        self.model.train(df)

    def run_once(self) -> Optional[int]:
        df = get_ohlc(self.symbol, self.timeframe, 100)
        signal, prob = self.model.predict(df)
        print(f"Signal: {signal}, probability: {prob:.2f}")
        if signal == 'HOLD':
            return None
        price = mt5.symbol_info_tick(self.symbol).ask if signal == 'BUY' else mt5.symbol_info_tick(self.symbol).bid
        lot = 0.1
        request = {
            'action': mt5.TRADE_ACTION_DEAL,
            'symbol': self.symbol,
            'volume': lot,
            'type': mt5.ORDER_TYPE_BUY if signal == 'BUY' else mt5.ORDER_TYPE_SELL,
            'price': price,
            'sl': 0,
            'tp': 0,
            'deviation': 20,
            'magic': 234000,
            'comment': 'AI trade',
            'type_time': mt5.ORDER_TIME_GTC,
            'type_filling': mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        print(f"order_send result: {result}")
        return result
