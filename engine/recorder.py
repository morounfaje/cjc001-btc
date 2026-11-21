import json
import os

import pandas as pd

import config
from engine import metrics


def save_run(strategy, df, trades, equity_curve, dataset_version):
    """Save everything needed to review and reproduce one backtest run."""
    folder = os.path.join("results", strategy.name)
    os.makedirs(folder, exist_ok=True)

    pd.DataFrame(trades).to_csv(os.path.join(folder, "trades.csv"), index=False)
    pd.DataFrame(equity_curve).to_csv(os.path.join(folder, "equity_curve.csv"), index=False)

    summary = {
        "strategy": strategy.name,
        "parameters": vars(strategy),
        "symbol": config.SYMBOL,
        "timeframe": config.TIMEFRAME,
        "dataset_version": dataset_version,
        "bars": len(df),
        "first_bar": str(df["timestamp"].iloc[0]),
        "last_bar": str(df["timestamp"].iloc[-1]),
        "holdout_fraction": config.HOLDOUT_FRACTION,
        "starting_cash": config.STARTING_CASH,
        "fee_rate": config.FEE_RATE,
        "slippage": config.SLIPPAGE,
        "total_return": metrics.total_return(equity_curve),
        "max_drawdown": metrics.max_drawdown(equity_curve),
        "sharpe": metrics.sharpe_ratio(equity_curve),
        **metrics.trade_stats(trades),
    }

    with open(os.path.join(folder, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    return folder