from strategies.base import Strategy


class SMACrossover(Strategy):
    """BUY when the fast average crosses above the slow one, SELL when it crosses below."""

    name = "sma_crossover"

    def __init__(self, fast=20, slow=50):
        if fast >= slow:
            raise ValueError("fast window must be smaller than slow window")
        self.fast = fast
        self.slow = slow

    def generate_signals(self, df):
        fast_avg = df["close"].rolling(self.fast).mean()
        slow_avg = df["close"].rolling(self.slow).mean()

        crossed_up = (fast_avg.shift(1) <= slow_avg.shift(1)) & (fast_avg > slow_avg)
        crossed_down = (fast_avg.shift(1) >= slow_avg.shift(1)) & (fast_avg < slow_avg)

        signals = ["HOLD"] * len(df)
        for i in range(len(df)):
            if crossed_up.iloc[i]:
                signals[i] = "BUY"
            elif crossed_down.iloc[i]:
                signals[i] = "SELL"
        return signals