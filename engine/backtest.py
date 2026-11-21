import config
from engine.portfolio import Portfolio


def run_backtest(df, strategy, starting_cash=config.STARTING_CASH):
    """Run one strategy over the price bars in df.

    The strategy gives a signal for every bar using data up to that bar.
    A signal from bar t is acted on at the OPEN of bar t+1, never sooner.
    Returns (trades, equity_curve).
    """
    signals = list(strategy.generate_signals(df))
    if len(signals) != len(df):
        raise ValueError("Strategy must return exactly one signal per bar")

    portfolio = Portfolio(starting_cash)
    trades = []
    equity_curve = []

    for i in range(len(df)):
        timestamp = df["timestamp"].iloc[i]

        if i > 0:
            signal = signals[i - 1]            # yesterday's signal...
            open_price = df["open"].iloc[i]    # ...acted on at today's open

            if signal == "BUY" and not portfolio.in_position():
                trade = portfolio.buy(open_price)
                trade["timestamp"] = timestamp
                trades.append(trade)
            elif signal == "SELL" and portfolio.in_position():
                trade = portfolio.sell(open_price)
                trade["timestamp"] = timestamp
                trades.append(trade)

        equity = portfolio.equity(df["close"].iloc[i])
        equity_curve.append({"timestamp": timestamp, "equity": equity})

    return trades, equity_curve