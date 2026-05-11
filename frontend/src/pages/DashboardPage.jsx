import { EquityChart } from "../charts/EquityChart.jsx";
import { MetricCard } from "../components/MetricCard.jsx";
import { SignalsTable } from "../components/SignalsTable.jsx";
import { TradeTable } from "../components/TradeTable.jsx";
import { useBacktest } from "../context/BacktestContext.jsx";

function money(n) {
  return Number(n).toLocaleString(undefined, { style: "currency", currency: "USD", maximumFractionDigits: 2 });
}

export function DashboardPage() {
  const { result, error, strategy } = useBacktest();

  const metrics = result?.metrics;
  const returnPct = metrics?.total_return_pct ?? 0;
  const showMlAccuracy = strategy === "ml" && Boolean(result?.ml_results);

  return (
    <div className="space-y-6">
      {error ? (
        <div className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
          {error}
        </div>
      ) : null}

      <section
        className={`grid gap-4 sm:grid-cols-2 ${
          showMlAccuracy ? "xl:grid-cols-5" : "xl:grid-cols-4"
        }`}
      >
        <MetricCard
          label="Final portfolio value"
          value={result ? money(result.final_portfolio_value) : "—"}
          sub={result ? `Initial: ${money(result.initial_balance)}` : "Run a backtest"}
        />
        <MetricCard
          label="Total return %"
          value={result ? `${returnPct.toFixed(2)}%` : "—"}
          highlight={returnPct > 0 ? "profit" : returnPct < 0 ? "loss" : undefined}
          sub="From your metrics helper"
        />
        <MetricCard
          label="Win rate %"
          value={result ? `${metrics.win_rate_pct.toFixed(2)}%` : "—"}
          sub="Based on sell trades in trade history"
        />
        <MetricCard
          label="Total trades"
          value={result ? String(metrics.total_trades) : "—"}
          sub="Completed sells counted by metrics"
        />
        {showMlAccuracy ? (
          <MetricCard
            label="ML accuracy"
            value={`${(result.ml_results.accuracy * 100).toFixed(2)}%`}
            sub="sklearn accuracy_score on test split"
          />
        ) : null}
      </section>

      <EquityChart data={result?.equity_curve} />

      <div className="grid gap-6 lg:grid-cols-2">
        <SignalsTable signals={result?.signals} />
        <TradeTable trades={result?.trades} />
      </div>
    </div>
  );
}
