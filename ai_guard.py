"""Local machine-learning gate for reducing noisy trades.

The model is trained only on the supplied historical bars and predicts whether
price is likely to move in the proposed direction over the next few bars.
It is deliberately fail-closed: insufficient data or weak confidence means
NO_TRADE.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


FEATURE_COLUMNS = [
    "return_1",
    "return_3",
    "return_5",
    "range_pct",
    "volatility",
    "volume_ratio",
    "sma_gap",
    "rsi",
]


@dataclass
class AIDecision:
    """Explainable output from the local trade gate."""

    action: str
    confidence: float
    regime: str
    reason: str


class AINoiseGate:
    """Train a small rolling classifier and abstain from weak trades."""

    def __init__(self, min_confidence=0.62, horizon=3, min_training_rows=35):
        self.min_confidence = min_confidence
        self.horizon = horizon
        self.min_training_rows = min_training_rows

    @staticmethod
    def _features(bars_df):
        close = pd.to_numeric(bars_df["c"], errors="coerce")
        high = pd.to_numeric(bars_df["h"], errors="coerce")
        low = pd.to_numeric(bars_df["l"], errors="coerce")
        volume = pd.to_numeric(bars_df["v"], errors="coerce")
        returns = close.pct_change()
        average_volume = volume.rolling(20).mean()
        sma = close.rolling(20).mean()
        gains = returns.clip(lower=0).rolling(14).mean()
        losses = -returns.clip(upper=0).rolling(14).mean()
        relative_strength = gains / losses.replace(0, np.nan)
        rsi = 100 - (100 / (1 + relative_strength))

        return pd.DataFrame(
            {
                "return_1": returns,
                "return_3": close.pct_change(3),
                "return_5": close.pct_change(5),
                "range_pct": (high - low) / close,
                "volatility": returns.rolling(10).std(),
                "volume_ratio": volume / average_volume,
                "sma_gap": (close - sma) / sma,
                "rsi": rsi,
            },
            index=bars_df.index,
        )

    def decide(self, bars_df, proposed_signal):
        """Return an AI-gated decision for BUY_CALL or BUY_PUT."""
        if proposed_signal not in {"BUY_CALL", "BUY_PUT"}:
            return AIDecision("NO_TRADE", 0.0, "unknown", "No directional signal to validate")

        if bars_df is None or len(bars_df) < self.min_training_rows + self.horizon + 10:
            return AIDecision(
                "NO_TRADE", 0.0, "insufficient_data", "Not enough history to train the gate"
            )

        features = self._features(bars_df)
        close = pd.to_numeric(bars_df["c"], errors="coerce")
        future_return = close.shift(-self.horizon) / close - 1
        usable = features[FEATURE_COLUMNS].replace([np.inf, -np.inf], np.nan).dropna().index
        training_index = usable.intersection(future_return.dropna().index)
        if len(training_index) < self.min_training_rows:
            return AIDecision("NO_TRADE", 0.0, "insufficient_data", "Not enough clean training rows")

        target = (future_return.loc[training_index] > 0).astype(int)
        if target.nunique() < 2:
            return AIDecision("NO_TRADE", 0.0, "one_sided", "Recent history has only one outcome class")

        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=4,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=42,
        )
        model.fit(features.loc[training_index, FEATURE_COLUMNS], target)

        latest = features.iloc[[-1]][FEATURE_COLUMNS].replace([np.inf, -np.inf], np.nan)
        if latest.isna().any(axis=None):
            return AIDecision("NO_TRADE", 0.0, "invalid_features", "Latest market features are incomplete")

        probabilities = model.predict_proba(latest)[0]
        bullish_probability = float(probabilities[list(model.classes_).index(1)])
        directional_probability = (
            bullish_probability if proposed_signal == "BUY_CALL" else 1 - bullish_probability
        )
        current_volatility = float(features["volatility"].iloc[-1])
        regime = "volatile" if current_volatility > float(features["volatility"].rolling(20).median().iloc[-1]) else "calm"

        if directional_probability < self.min_confidence:
            return AIDecision(
                "NO_TRADE",
                directional_probability,
                regime,
                f"Model confidence {directional_probability:.1%} is below the threshold",
            )

        return AIDecision(
            proposed_signal,
            directional_probability,
            regime,
            f"Model agrees with {proposed_signal} at {directional_probability:.1%} confidence",
        )
