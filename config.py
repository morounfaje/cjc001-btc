# Asset-specific settings for CJC001-BTC.
# Anything that changes between assets lives here and nowhere else.

SYMBOL = "BTC-USD"
TIMEFRAME = "1h"

STARTING_CASH = 10_000

FEE_RATE = 0.001          # 0.1% of trade value, charged on every buy and sell
SLIPPAGE = 0.0005         # fills 0.05% worse than the bar's open price

BARS_PER_YEAR = 24 * 365  # hourly bars; Bitcoin trades 24/7

HOLDOUT_FRACTION = 0.25   # last 25% of the data stays untouched until the final test