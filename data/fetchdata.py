import ccxt
import pandas as pd
import time


exchange = ccxt.binance()

symbol = "BTC/USDT"

timeframe = "1h"

since = exchange.parse8601(
    "2022-01-01T00:00:00Z"
)

all_candles = []


while True:

    ohlcv = exchange.fetch_ohlcv(
        symbol,
        timeframe=timeframe,
        since=since,
        limit=1000
    )

    if len(ohlcv) == 0:
        break

    all_candles.extend(ohlcv)

    since = ohlcv[-1][0] + 1

    print(
        f"Fetched {len(all_candles)} candles..."
    )

    time.sleep(1)


headers = [
    "Timestamp",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

df = pd.DataFrame(
    all_candles,
    columns=headers
)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    unit="ms",
    utc=True
)

df.drop_duplicates(
    subset=["Timestamp"],
    inplace=True
)

df.reset_index(
    drop=True,
    inplace=True
)

print(df.head())

print(df.tail())

print(f"\nTotal Candles: {len(df)}")


df.to_csv(
    "data/BTCUSDT_1h.csv",
    index=False
)

print("\nDataset Saved Successfully.")