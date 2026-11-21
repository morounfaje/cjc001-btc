class Strategy:
    """Base class. Every strategy inherits from this.

    RULE: the signal for bar t may only use data from bar t and earlier.
    The engine will act on it from bar t+1.
    """

    name = "base"

    def generate_signals(self, df):
        """Take a table of OHLC bars. Return one signal per bar:
        'BUY', 'SELL' or 'HOLD'."""
        raise NotImplementedError("Each strategy must implement generate_signals")