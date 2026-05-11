from strategy.indicators import indicators
from strategy.signals import generate_sginals

from ml.prepare_data import prepare_ml_data
from ml.train_model import train_ml_model
from ml.predict import generate_ml_signals

from backtester.engine import Backtester

from utils.metrics import calculate_metrics

import pandas as pd
import matplotlib.pyplot as plt


# =========================
# USER CONFIG
# =========================

USE_ML = False

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


# =========================
# ENSURE TIMESTAMP FORMAT
# =========================

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    utc=True
)


# =========================
# SORT DATA
# =========================

df.sort_values(
    "Timestamp",
    inplace=True
)


# =========================
# ML MODEL TRAINING
# =========================

X, y, ml_df = prepare_ml_data(df)

model, predictions, y_test = train_ml_model(X, y)


# =========================
# FILTER DATE RANGE
# =========================

filtered_df = df[
    (df["Timestamp"] >= start_date) &
    (df["Timestamp"] <= end_date)
].copy()


# =========================
# CALCULATE INDICATORS
# =========================

result = indicators(filtered_df)


# =========================
# SIGNAL GENERATION
# =========================

if USE_ML:

    print("\nUSING ML STRATEGY\n")

    result = generate_ml_signals(
        model,
        result
    )

else:

    print("\nUSING RULE-BASED STRATEGY\n")

    result = generate_sginals(result)


# =========================
# PREVIEW SIGNALS
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
# CALCULATE METRICS
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