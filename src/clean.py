import pandas as pd
import os
from ingest import TICKERS, ALL_TICKERS

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

SECTOR_MAP = {ticker: sector for sector, tickers in TICKERS.items() for ticker in tickers}


def load_and_clean(ticker):
    """Load raw CSV for a ticker, standardize format, validate integrity."""
    path = os.path.join(RAW_DIR, f"{ticker}.csv")
    df = pd.read_csv(path, parse_dates=["Date"])

    # sort and set date as index
    df = df.sort_values("Date")
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df = df.set_index("Date")

    # dtypes
    for col in ["Open", "High", "Low", "Close"]:
        df[col] = df[col].astype(float)
    df["Volume"] = df["Volume"].astype(int)

    # drop duplicate dates
    n_dupes = df.index.duplicated().sum()
    if n_dupes > 0:
        print(f"  WARNING: {ticker} dropping {n_dupes} duplicate dates")
        df = df[~df.index.duplicated(keep="first")]

    # drop bad OHLC rows
    bad_ohlc = (df["High"] < df["Low"]).sum()
    if bad_ohlc > 0:
        print(f"  WARNING: {ticker} dropping {bad_ohlc} bad OHLC rows")
        df = df[df["High"] >= df["Low"]]

    # drop zero volume rows
    zero_vol = (df["Volume"] == 0).sum()
    if zero_vol > 0:
        print(f"  WARNING: {ticker} dropping {zero_vol} zero volume rows")
        df = df[df["Volume"] > 0]

    # add metadata
    df["ticker"] = ticker
    df["sector"] = SECTOR_MAP[ticker]

    return df


def clean_all(tickers=None):
    """Clean all tickers and save to data/processed/."""
    if tickers is None:
        tickers = ALL_TICKERS

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    for ticker in tickers:
        print(f"Cleaning {ticker}...")
        df = load_and_clean(ticker)
        out_path = os.path.join(PROCESSED_DIR, f"{ticker}.csv")
        df.to_csv(out_path)
        print(f"  saved at processed/{ticker}.csv")

    print("\nall tickers cleaned and saved.")


if __name__ == "__main__":
    clean_all()