# app.py

from strategy.indicators import indicators
from strategy.signals import generate_sginals

from backtester.engine import Backtester

import pandas as pd
import matplotlib.pyplot as plt

from utils.metrics import calculate_metrics

from ml.prepare_data import prepare_ml_data
from ml.train_model import train_ml_model
from ml.predict import generate_ml_signals


# =========================
# CONFIG
# =========================

USE_ML = True

initial_balance = 10000

start_date = "2023-02-15"
end_date = "2023-03-05"


# =========================
# LOAD DATA
# =========================

df = pd.read_csv(
    "data/BTCUSDT_1h.csv",
    parse_dates=["Timestamp"]
)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    utc=True
)

df.sort_values("Timestamp", inplace=True)


# =========================
# PREPARE ML DATA
# =========================

X, y, ml_df = prepare_ml_data(df)


# =========================
# TRAIN MODEL
# =========================

model, X_test, y_test = train_ml_model(X, y)


# =========================
# FILTER DATE RANGE
# =========================

filtered_df = ml_df[
    (ml_df["Timestamp"] >= start_date) &
    (ml_df["Timestamp"] <= end_date)
].copy()


# =========================
# STRATEGY SELECTION
# =========================

if USE_ML:

    print("\nUSING ML STRATEGY\n")

    result = generate_ml_signals(
        model=model,
        df=filtered_df
    )

else:

    print("\nUSING RULE-BASED STRATEGY\n")

    result = indicators(filtered_df)

    result = generate_sginals(result)


# =========================
# SHOW DATA
# =========================

print(result[[
    "Timestamp",
    "Close",
    "SMA20",
    "SMA50",
    "RSI",
    "Signals"
]].tail(20))


# =========================
# RUN BACKTEST
# =========================

backtester = Backtester(
    result,
    initial_balance=initial_balance
)

backtest_results = backtester.run()


# =========================
# OUTPUT RESULTS
# =========================

print("\nFinal Portfolio Value:")

print(backtest_results["final_value"])


print("\nTrade History:")

for trade in backtest_results["trade_history"][:10]:

    print(trade)


# =========================
# METRICS
# =========================

metrics = calculate_metrics(
    backtester.initial_balance,
    backtest_results["final_value"],
    backtest_results["trade_history"]
)

print("\nMetrics : ")

print(metrics)


# =========================
# EQUITY CURVE
# =========================

plt.figure(figsize=(15, 6))

plt.plot(
    backtest_results["portfolio_values"]
)

if USE_ML:
    plt.title("ML Strategy Equity Curve")
else:
    plt.title("Rule-Based Strategy Equity Curve")

plt.xlabel("Trades")
plt.ylabel("Portfolio Value")

plt.grid()

plt.show()