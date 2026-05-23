import yfinance as yf
import os

TICKERS = {
    "tech": ["AAPL", "MSFT", "GOOGL"],
    "finance": ["JPM", "GS", "BAC"],
    "energy": ["XOM", "CVX"],
    "consumer": ["AMZN", "WMT"],
    "semiconductors": ["NVDA", "AMD"],
    "healthcare": ["JNJ", "PFE"],
}

ALL_TICKERS = [t for sector in TICKERS.values() for t in sector]

START_DATE = "2019-01-01"
END_DATE = "2024-12-31"

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

def download_data(tickers = ALL_TICKERS, start = START_DATE, end = END_DATE):
    """Download the data from yfinance and save it."""
    os.makedirs(RAW_DIR, exist_ok=True)

    for ticker in tickers:
        print(f"Downloading {ticker} ...")
        df = yf.download(ticker, start=start, end=end, auto_adjust=True, multi_level_index=False)

        if df.empty:
            print (f"No data available for {ticker}, skipping")
            continue

        df.index = df.index.tz_localize(None)
        csv_path = os.path.join(RAW_DIR, f"{ticker}.csv")
        df.to_csv(csv_path)

        json_path = os.path.join(RAW_DIR, f"{ticker}.json")
        df.to_json(json_path, orient="index", date_format="iso")

        print(f"saved {ticker} to CSV and JSON")

    print("\nall tickers downloaded.")

if __name__ == "__main__":
    download_data()