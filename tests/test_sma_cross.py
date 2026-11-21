import math

import pandas as pd
import pytest

from strategies.sma_cross import SMACrossover


def make_bars(closes):
    return pd.DataFrame({
        "timestamp": pd.date_range("2026-01-01", periods=len(closes), freq="h", tz="UTC"),
        "open": closes,
        "high": closes,
        "low": closes,
        "close": closes,
    })


def test_known_crossovers():
    # with windows of 2 and 3, these closes cross up at bar 4 and down at bar 6
    df = make_bars([10, 10, 10, 10, 20, 20, 5, 5, 5])
    signals = SMACrossover(fast=2, slow=3).generate_signals(df)

    assert signals == ["HOLD", "HOLD", "HOLD", "HOLD", "BUY",
                       "HOLD", "SELL", "HOLD", "HOLD"]


def test_signals_do_not_depend_on_future_bars():
    closes = [100 + 10 * math.sin(i / 5) + i * 0.05 for i in range(200)]
    df = make_bars(closes)
    strategy = SMACrossover(fast=5, slow=15)
    full = strategy.generate_signals(df)

    assert any(s != "HOLD" for s in full)      # the test must contain real signals

    for cut in range(40, 200):
        partial = strategy.generate_signals(df.iloc[:cut])
        assert partial == full[:cut]


def test_fast_window_must_be_smaller_than_slow():
    with pytest.raises(ValueError):
        SMACrossover(fast=50, slow=20)