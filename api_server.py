"""
Lightweight HTTP API for the existing backtesting flow (same steps as app.py).
Does not modify engine, strategy, or ML module internals.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.metrics import accuracy_score, classification_report

from backtester.engine import Backtester
from ml.prepare_data import prepare_ml_data
from ml.predict import generate_ml_signals
from ml.train_model import train_ml_model
from strategy.indicators import indicators
from strategy.signals import generate_sginals
from utils.metrics import calculate_metrics

app = FastAPI(title="BTC Backtesting API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _resolve_csv_path() -> Path:
    root = Path(__file__).resolve().parent
    for name in ("data/BTCUSDT_1h.csv", "data/BTCUSDT1hr.csv", "data/btc_data.csv"):
        p = root / name
        if p.is_file():
            return p
    raise FileNotFoundError(
        "No OHLCV CSV found. Expected one of: data/BTCUSDT_1h.csv, "
        "data/BTCUSDT1hr.csv, data/btc_data.csv"
    )


def _ts_iso(val: Any) -> str:
    return pd.Timestamp(val).isoformat()


class RunBacktestBody(BaseModel):
    strategy: Literal["rule", "ml"]
    start_date: str
    end_date: str
    initial_balance: float = Field(10_000, gt=0)


def _run_pipeline(body: RunBacktestBody) -> dict[str, Any]:
    csv_path = _resolve_csv_path()
    df = pd.read_csv(csv_path, parse_dates=["Timestamp"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
    df.sort_values("Timestamp", inplace=True)

    X, y, ml_df = prepare_ml_data(df)
    model, X_test, y_test = train_ml_model(X, y)

    test_predictions = model.predict(X_test)
    accuracy = float(accuracy_score(y_test, test_predictions))
    report = classification_report(y_test, test_predictions)

    prediction_rows: list[dict[str, Any]] = []
    for idx, pred in zip(X_test.index, test_predictions):
        prediction_rows.append(
            {
                "timestamp": _ts_iso(ml_df.loc[idx, "Timestamp"]),
                "actual": int(y_test.loc[idx]),
                "predicted": int(pred),
            }
        )

    filtered_df = ml_df[
        (ml_df["Timestamp"] >= body.start_date) & (ml_df["Timestamp"] <= body.end_date)
    ].copy()

    if filtered_df.empty:
        raise HTTPException(status_code=400, detail="No rows in selected date range.")

    if body.strategy == "ml":
        result = generate_ml_signals(model=model, df=filtered_df)
    else:
        result = indicators(filtered_df)
        result = generate_sginals(result)

    backtester = Backtester(result, initial_balance=body.initial_balance)
    backtest_results = backtester.run()

    metrics = calculate_metrics(
        backtester.initial_balance,
        backtest_results["final_value"],
        backtest_results["trade_history"],
    )

    trades_out: list[dict[str, Any]] = []
    for t in backtest_results["trade_history"]:
        row: dict[str, Any] = {
            "timestamp": _ts_iso(t["Timestamp"]),
            "type": t["Type"],
            "price": float(t["Price"]),
        }
        if t["Type"] == "SELL" and "Profit %" in t:
            row["profit_pct"] = float(t["Profit %"])
        else:
            row["profit_pct"] = None
        trades_out.append(row)

    signals_out: list[dict[str, Any]] = []
    for _, r in result.iterrows():
        signals_out.append(
            {
                "timestamp": _ts_iso(r["Timestamp"]),
                "close": float(r["Close"]),
                "sma20": float(r["SMA20"]),
                "sma50": float(r["SMA50"]),
                "rsi": float(r["RSI"]),
                "signal": int(r["Signals"]),
            }
        )

    equity_curve: list[dict[str, Any]] = []
    for i, val in enumerate(backtest_results["portfolio_values"]):
        equity_curve.append(
            {
                "timestamp": _ts_iso(result["Timestamp"].iloc[i]),
                "value": float(val),
            }
        )

    return {
        "strategy": body.strategy,
        "start_date": body.start_date,
        "end_date": body.end_date,
        "initial_balance": float(body.initial_balance),
        "final_portfolio_value": float(backtest_results["final_value"]),
        "metrics": {
            "total_return_pct": metrics["Total Return %"],
            "total_trades": metrics["Total Trades"],
            "win_rate_pct": metrics["Win Rate %"],
        },
        "portfolio_values": [float(v) for v in backtest_results["portfolio_values"]],
        "equity_curve": equity_curve,
        "trades": trades_out,
        "signals": signals_out,
        "ml_results": {
            "accuracy": accuracy,
            "classification_report": report,
            "predictions": prediction_rows,
        },
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/run_backtest")
def run_backtest(body: RunBacktestBody) -> dict[str, Any]:
    try:
        return _run_pipeline(body)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/metrics")
def metrics_endpoint(body: RunBacktestBody) -> dict[str, Any]:
    data = _run_pipeline(body)
    return {
        "metrics": data["metrics"],
        "final_portfolio_value": data["final_portfolio_value"],
        "strategy": data["strategy"],
    }


@app.post("/trades")
def trades_endpoint(body: RunBacktestBody) -> dict[str, Any]:
    data = _run_pipeline(body)
    return {"trades": data["trades"]}


@app.post("/signals")
def signals_endpoint(body: RunBacktestBody) -> dict[str, Any]:
    data = _run_pipeline(body)
    return {"signals": data["signals"]}


@app.post("/ml_results")
def ml_results_endpoint(body: RunBacktestBody) -> dict[str, Any]:
    data = _run_pipeline(body)
    return {"ml_results": data["ml_results"]}
