import yfinance as yf
import config

OUT_PATH = "data/btc_1h.csv"


def download():
    df = yf.download(config.SYMBOL, period="2y", interval=config.TIMEFRAME)

    # newer yfinance returns two-level column names; flatten to simple names
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    df = df.reset_index()
    df = df.rename(columns={
        "Datetime": "timestamp",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    })
    df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]

    # drop the newest candle: it is still forming, and a backtest must only see finished bars
    df = df.iloc[:-1]
    return df


if __name__ == "__main__":
    df = download()
    df.to_csv(OUT_PATH, index=False)
    print("Saved", len(df), "rows to", OUT_PATH)
    print(df.head(3))
    print(df.tail(3))