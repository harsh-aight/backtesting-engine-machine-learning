import pandas as pd


def generate_ml_signals(model, df):

    # =========================
    # FEATURE COLUMNS
    # =========================

    feature_columns = [
        "SMA20",
        "SMA50",
        "RSI",
        "MACD",
        "MACD_SIGNAL"
    ]

    # =========================
    # PREPARE FEATURES
    # =========================

    features = df[feature_columns].copy()

    features.dropna(inplace=True)

    # =========================
    # MODEL PREDICTIONS
    # =========================

    predictions = model.predict(features)

    # =========================
    # CONVERT TO SIGNALS
    # =========================

    signals = []

    for pred in predictions:

        # BUY SIGNAL
        if pred == 1:

            signals.append(1)

        # SELL SIGNAL
        else:

            signals.append(-1)

    # =========================
    # ALIGN DATAFRAME
    # =========================

    result_df = df.iloc[-len(signals):].copy()

    result_df["Signals"] = signals

    return result_df