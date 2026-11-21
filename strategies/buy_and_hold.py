from strategies.base import Strategy


class BuyAndHold(Strategy):
    """Benchmark: buy at the start, never sell. Every real strategy must beat this."""

    name = "buy_and_hold"

    def generate_signals(self, df):
        return ["BUY"] + ["HOLD"] * (len(df) - 1)