import pandas as pd

from strategy.indicators import indicators


def prepare_ml_data(df):

    # =========================
    # ADD INDICATORS
    # =========================

    df = indicators(df)


    # =========================
    # CREATE TARGET COLUMN
    # =========================

    # 1 = NEXT CANDLE GOES UP
    # 0 = NEXT CANDLE GOES DOWN

    df["Target"] = (
        df["Close"].shift(-1) > df["Close"]
    ).astype(int)


    # =========================
    # SELECT FEATURES
    # =========================

    features = [
        "SMA20",
        "SMA50",
        "RSI",
        "MACD",
        "MACD_SIGNAL"
    ]


    # =========================
    # REMOVE NaN VALUES
    # =========================

    df.dropna(inplace=True)


    # =========================
    # CREATE X AND y
    # =========================

    X = df[features]

    y = df["Target"]


    # =========================
    # DEBUG OUTPUT
    # =========================

    print("\nML DATA PREP COMPLETE\n")

    print("Features Shape:")

    print(X.shape)

    print("\nTarget Shape:")

    print(y.shape)

    print("\nFeature Preview:\n")

    print(X.head())

    print("\nTarget Preview:\n")

    print(y.head())
    print("function running ")

    return X, y, df