import ccxt
import pandas as pd
import time


# =========================
# EXCHANGE CONFIG
# =========================

exchange = ccxt.binance()

symbol = "BTC/USDT"

timeframe = "1h"

since = exchange.parse8601(
    "2022-01-01T00:00:00Z"
)


# =========================
# FETCH DATA
# =========================

all_candles = []


while True:

    ohlcv = exchange.fetch_ohlcv(
        symbol,
        timeframe=timeframe,
        since=since,
        limit=1000
    )

    # STOP IF NO MORE DATA
    if len(ohlcv) == 0:
        break

    all_candles.extend(ohlcv)

    # MOVE TO NEXT BATCH
    since = ohlcv[-1][0] + 1

    print(
        f"Fetched {len(all_candles)} candles..."
    )

    # PREVENT RATE LIMIT ISSUES
    time.sleep(1)


# =========================
# CREATE DATAFRAME
# =========================

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


# =========================
# CLEANING
# =========================

# CONVERT TIMESTAMP
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    unit="ms",
    utc=True
)

# ENSURE NUMERIC TYPES
numeric_cols = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

df[numeric_cols] = (
    df[numeric_cols]
    .astype(float)
)

# REMOVE DUPLICATES
df.drop_duplicates(
    subset=["Timestamp"],
    inplace=True
)

# REMOVE NULL VALUES
df.dropna(inplace=True)

# SORT BY TIME
df.sort_values(
    "Timestamp",
    inplace=True
)

# RESET INDEX
df.reset_index(
    drop=True,
    inplace=True
)


# =========================
# DATA VALIDATION
# =========================

print("\nDATA INFO:\n")

print(df.info())

print("\nFIRST 5 ROWS:\n")

print(df.head())

print("\nLAST 5 ROWS:\n")

print(df.tail())

print(f"\nTotal Candles: {len(df)}")


# =========================
# SAVE DATASET
# =========================

df.to_csv(
    "BTCUSDT_1h.csv",
    index=False
)

print("\nDataset Saved Successfully.")