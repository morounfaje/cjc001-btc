import math

import config



def total_return(equity_curve):
    """Overall gain or loss as a fraction of the starting value (0.10 = +10%)."""
    start = equity_curve[0]["equity"]
    end = equity_curve[-1]["equity"]
    return (end - start) / start


def max_drawdown(equity_curve):
    """Worst fall from a previous peak, as a negative fraction (-0.30 = -30%)."""
    peak = equity_curve[0]["equity"]
    worst = 0.0

    for point in equity_curve:
        equity = point["equity"]
        if equity > peak:
            peak = equity
        drawdown = (equity - peak) / peak
        if drawdown < worst:
            worst = drawdown

    return worst


def trade_stats(trades):
    """Win rate and average win/loss over closed trades (each SELL closes one)."""
    profits = [t["profit"] for t in trades if t["action"] == "SELL"]

    if not profits:
        return {"trade_count": 0, "win_rate": 0.0,
                "avg_win": 0.0, "avg_loss": 0.0, "avg_trade": 0.0}

    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p <= 0]

    return {
        "trade_count": len(profits),
        "win_rate": len(wins) / len(profits),
        "avg_win": sum(wins) / len(wins) if wins else 0.0,
        "avg_loss": sum(losses) / len(losses) if losses else 0.0,
        "avg_trade": sum(profits) / len(profits),
    }



def sharpe_ratio(equity_curve, bars_per_year=config.BARS_PER_YEAR):
    """Annualised return per unit of risk. Risk-free rate is assumed to be zero."""
    equities = [point["equity"] for point in equity_curve]
    returns = [(equities[i] - equities[i - 1]) / equities[i - 1]
               for i in range(1, len(equities))]

    average = sum(returns) / len(returns)
    variance = sum((r - average) ** 2 for r in returns) / len(returns)
    std_dev = math.sqrt(variance)

    if std_dev < 1e-12:          # effectively no movement at all
        return 0.0

    return (average / std_dev) * math.sqrt(bars_per_year)