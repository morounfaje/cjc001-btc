import pandas as pd
import pytest

import config
from engine.backtest import run_backtest
from strategies.base import Strategy


class FixedSignals(Strategy):
    """Test strategy that returns whatever signals we hand it."""

    def __init__(self, signals):
        self.signals = signals

    def generate_signals(self, df):
        return self.signals


def make_bars():
    """5 bars with open prices 10, 20, 30, 40, 50 so fill prices are easy to read."""
    return pd.DataFrame({
        "timestamp": pd.date_range("2026-01-01", periods=5, freq="h", tz="UTC"),
        "open":  [10, 20, 30, 40, 50],
        "high":  [10, 20, 30, 40, 50],
        "low":   [10, 20, 30, 40, 50],
        "close": [10, 20, 30, 40, 50],
    })


def test_buy_signal_fills_on_next_bar_open():
    df = make_bars()
    strategy = FixedSignals(["HOLD", "BUY", "HOLD", "HOLD", "HOLD"])
    trades, equity_curve = run_backtest(df, strategy)

    assert len(trades) == 1
    assert trades[0]["timestamp"] == df["timestamp"].iloc[2]   # bar 2, NOT bar 1
    assert abs(trades[0]["price"] - 30 * (1 + config.SLIPPAGE)) < 1e-9   # bar 2's open
    assert len(equity_curve) == 5


def test_signal_on_last_bar_is_never_traded():
    df = make_bars()
    strategy = FixedSignals(["HOLD", "HOLD", "HOLD", "HOLD", "BUY"])
    trades, equity_curve = run_backtest(df, strategy)

    assert trades == []          # there is no next bar to trade on


def test_wrong_number_of_signals_is_rejected():
    df = make_bars()
    strategy = FixedSignals(["HOLD", "BUY"])
    with pytest.raises(ValueError):
        run_backtest(df, strategy)