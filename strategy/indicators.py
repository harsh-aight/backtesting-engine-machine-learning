import ta
import pandas
def indicators(df):
    df["SMA20"] = df["Close"].rolling(window=20).mean()
    df["SMA50"] = df["Close"].rolling(window=50).mean()
    df["RSI"] = ta.momentum.RSIIndicator(close = df["Close"]).rsi()
    macd = ta.trend.MACD(close = df["Close"])
    df["MACD"]= macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df.dropna(inplace=True)
    return df
