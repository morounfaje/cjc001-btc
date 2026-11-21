import config
from data.loader import load_data
from engine.backtest import run_backtest
from engine import metrics
from strategies.sma_cross import SMACrossover
from strategies.buy_and_hold import BuyAndHold


def development_data(df):
    """Return only the first part of the data. The last HOLDOUT_FRACTION stays sealed."""
    cut = int(len(df) * (1 - config.HOLDOUT_FRACTION))
    return df.iloc[:cut]


def report(name, df, strategy):
    trades, equity_curve = run_backtest(df, strategy)
    stats = metrics.trade_stats(trades)

    print(name)
    print("  total return :", round(metrics.total_return(equity_curve) * 100, 2), "%")
    print("  max drawdown :", round(metrics.max_drawdown(equity_curve) * 100, 2), "%")
    print("  sharpe       :", round(metrics.sharpe_ratio(equity_curve), 2))
    print("  closed trades:", stats["trade_count"])
    print("  win rate     :", round(stats["win_rate"] * 100, 1), "%")
    print("  avg win/loss :", round(stats["avg_win"], 2), "/", round(stats["avg_loss"], 2))
    print("  avg trade    :", round(stats["avg_trade"], 2))
    print()


if __name__ == "__main__":
    df = development_data(load_data())
    print("Development data:", len(df), "bars,",
          df["timestamp"].iloc[0], "to", df["timestamp"].iloc[-1])
    print()

    report("SMA 20/50 crossover", df, SMACrossover(20, 50))
    report("Buy and hold", df, BuyAndHold())