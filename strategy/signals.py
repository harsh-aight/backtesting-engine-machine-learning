import pandas

def generate_sginals(df):
    signals = []
    for i in range(len(df)):
        buy_condition = (df["SMA20"].iloc[i]>df["SMA50"].iloc[i] and df["RSI"].iloc[i]<70)
        sell_condition = (df["SMA20"].iloc[i]<df["SMA50"].iloc[i])
        if buy_condition:
            signals.append(1)
        elif sell_condition:
            signals.append(-1)
        else:
            signals.append(0)
    df["Signals"] = signals
    return df 