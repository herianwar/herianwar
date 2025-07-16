import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Tuple
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create technical indicators as features."""
    df = df.copy()
    df['ema_fast'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=26, adjust=False).mean()
    df['rsi'] = compute_rsi(df['close'])
    df['macd'] = df['ema_fast'] - df['ema_slow']
    df = df.dropna()
    return df


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


@dataclass
class TradingModel:
    model: XGBClassifier | None = None

    def train(self, df: pd.DataFrame) -> None:
        df = create_features(df)
        X = df[['ema_fast', 'ema_slow', 'rsi', 'macd']]
        y = (df['close'].shift(-1) > df['close']).astype(int)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = XGBClassifier(eval_metric='logloss')
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"Training accuracy: {acc:.2f}")

    def predict(self, df: pd.DataFrame) -> Tuple[str, float]:
        if self.model is None:
            raise RuntimeError("Model is not trained")
        df = create_features(df.tail(1))
        proba = self.model.predict_proba(df[['ema_fast', 'ema_slow', 'rsi', 'macd']])[0][1]
        if proba > 0.55:
            return 'BUY', proba
        elif proba < 0.45:
            return 'SELL', proba
        else:
            return 'HOLD', proba
