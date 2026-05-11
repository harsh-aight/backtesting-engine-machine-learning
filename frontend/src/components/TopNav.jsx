import { Link, useLocation } from "react-router-dom";

export function TopNav({
  strategy,
  onStrategyChange,
  onRun,
  loading,
  startDate,
  endDate,
  initialBalance,
  onStartChange,
  onEndChange,
  onBalanceChange,
}) {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-20 border-b border-surface-border bg-surface-card/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
        <div className="flex flex-col gap-1">
          <h1 className="text-lg font-semibold tracking-tight text-white sm:text-xl">
            BTC ML Backtesting Dashboard
          </h1>
          <p className="text-xs text-slate-500">
            Visualizes outputs from your existing Python backtesting engine.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex rounded-lg border border-surface-border bg-surface p-0.5">
            <button
              type="button"
              onClick={() => onStrategyChange("rule")}
              className={`rounded-md px-3 py-1.5 text-sm font-medium transition ${
                strategy === "rule"
                  ? "bg-slate-700 text-white shadow"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              Rule-Based Strategy
            </button>
            <button
              type="button"
              onClick={() => onStrategyChange("ml")}
              className={`rounded-md px-3 py-1.5 text-sm font-medium transition ${
                strategy === "ml"
                  ? "bg-slate-700 text-white shadow"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              ML Strategy
            </button>
          </div>

          <Link
            to="/ml"
            className={`rounded-lg border px-3 py-2 text-sm font-medium transition ${
              location.pathname === "/ml"
                ? "border-accent text-accent"
                : "border-surface-border text-slate-300 hover:border-slate-500"
            }`}
          >
            ML Results
          </Link>

          <div className="hidden h-8 w-px bg-surface-border lg:block" />

          <div className="flex flex-wrap items-end gap-2">
            <label className="flex flex-col text-[10px] font-medium uppercase tracking-wide text-slate-500">
              Start
              <input
                type="date"
                value={startDate}
                onChange={(e) => onStartChange(e.target.value)}
                className="mt-0.5 rounded-md border border-surface-border bg-surface px-2 py-1.5 text-sm text-white"
              />
            </label>
            <label className="flex flex-col text-[10px] font-medium uppercase tracking-wide text-slate-500">
              End
              <input
                type="date"
                value={endDate}
                onChange={(e) => onEndChange(e.target.value)}
                className="mt-0.5 rounded-md border border-surface-border bg-surface px-2 py-1.5 text-sm text-white"
              />
            </label>
            <label className="flex flex-col text-[10px] font-medium uppercase tracking-wide text-slate-500">
              Initial balance
              <input
                type="number"
                min={1}
                step={100}
                value={initialBalance}
                onChange={(e) => onBalanceChange(Number(e.target.value))}
                className="mt-0.5 w-28 rounded-md border border-surface-border bg-surface px-2 py-1.5 text-sm text-white"
              />
            </label>
          </div>

          <button
            type="button"
            onClick={onRun}
            disabled={loading}
            className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-emerald-900/30 transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Running…" : "Run Backtest"}
          </button>
        </div>
      </div>
    </header>
  );
}
