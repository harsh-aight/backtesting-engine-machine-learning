# ml/predict.py

from strategy.indicators import indicators


def generate_ml_signals(model, df):

    # =========================
    # ADD INDICATORS
    # =========================

    df = indicators(df)

    # =========================
    # FEATURES
    # =========================

    features = df[[
        "SMA20",
        "SMA50",
        "RSI",
        "MACD",
        "MACD_SIGNAL"
    ]]

    # =========================
    # PREDICT
    # =========================

    predictions = model.predict(features)

    # =========================
    # CREATE SIGNALS
    # =========================

    signals = []

    for pred in predictions:

        if pred == 1:
            signals.append(1)

        else:
            signals.append(-1)

    df["Signals"] = signals

    # =========================
    # PREVENT LOOKAHEAD BIAS
    # =========================

    df["Signals"] = df["Signals"].shift(1)

    # =========================
    # REMOVE NAN
    # =========================

    df.dropna(inplace=True)

    return df