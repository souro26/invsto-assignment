import pandas as pd
import numpy as np


def compute_rsi(series, window=14):
    """Compute RSI for a price series."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def build_features(df):
    """Takes a cleaned OHLCV dataframe for a single ticker and returns a dataframe with features and target variable."""
    feat = pd.DataFrame(index=df.index)

    feat["return"] = df["Close"].pct_change()

    for lag in [1, 5, 10, 20]:
        feat[f"return_lag_{lag}"] = feat["return"].shift(lag)

    for window in [5, 20]:
        feat[f"rolling_vol_{window}"] = (
            feat["return"].rolling(window).std() * np.sqrt(252)
        )

    feat["volume_ratio"] = df["Volume"] / df["Volume"].rolling(5).mean()

    ma5 = df["Close"].rolling(5).mean()
    ma20 = df["Close"].rolling(20).mean()
    feat["ma_crossover"] = ma5 / ma20 - 1
    feat["rsi_14"] = compute_rsi(df["Close"], window=14)
    feat["target"] = feat["return"].shift(-1)
    feat["ticker"] = df["ticker"]
    feat["sector"] = df["sector"]
    feat = feat.dropna()

    return feat


def build_all_features(processed_dir, tickers):
    """Build features for all tickers and return combined dataframe."""
    all_dfs = []

    for ticker in tickers:
        df = pd.read_csv(
            f"{processed_dir}{ticker}.csv",
            parse_dates=["Date"],
            index_col="Date"
        )
        feat = build_features(df)
        all_dfs.append(feat)
        print(f"  {ticker}: {len(feat)} rows, {len(feat.columns)} columns")

    combined = pd.concat(all_dfs)
    print(f"\nTotal: {len(combined)} rows across {len(tickers)} tickers")
    return combined