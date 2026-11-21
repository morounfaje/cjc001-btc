import hashlib
import pandas as pd


class DataValidationError(ValueError):
    """Raised when the price data has a problem."""


REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close"]
PRICE_COLUMNS = ["open", "high", "low", "close"]


def validate(df):
    """Check a price table. Raise DataValidationError if anything is wrong."""
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise DataValidationError("Missing column: " + col)

    if df[REQUIRED_COLUMNS].isna().any().any():
        raise DataValidationError("Found missing (empty) values")

    if df["timestamp"].duplicated().any():
        raise DataValidationError("Found duplicate timestamps")

    if not df["timestamp"].is_monotonic_increasing:
        raise DataValidationError("Timestamps are not in ascending order")

    if (df[PRICE_COLUMNS] <= 0).any().any():
        raise DataValidationError("Found a price that is zero or negative")

    if (df["high"] < df["low"]).any():
        raise DataValidationError("Found a bar where high is below low")

    return df


def load_data(path="data/btc_1h.csv"):
    """Read the CSV, turn timestamps into real dates, validate, and return the table."""
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return validate(df)


def file_version(path="data/btc_1h.csv"):
    """A short fingerprint of the data file. Change one number in the file and this changes."""
    with open(path, "rb") as f:
        contents = f.read()
    return hashlib.sha256(contents).hexdigest()[:16]