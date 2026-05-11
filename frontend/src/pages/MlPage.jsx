import { Link } from "react-router-dom";
import { useBacktest } from "../context/BacktestContext.jsx";

export function MlPage() {
  const { result } = useBacktest();
  const ml = result?.ml_results;

  if (!result || !ml) {
    return (
      <div className="rounded-xl border border-surface-border bg-surface-card p-8 text-center">
        <p className="text-sm text-slate-400">Run a backtest first to load ML outputs from your engine.</p>
        <Link to="/" className="mt-4 inline-block text-sm font-medium text-accent hover:underline">
          Go to dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-white">ML training outputs</h2>
          <p className="text-sm text-slate-500">
            Accuracy, classification report, and test predictions — same artifacts your training script
            produces.
          </p>
        </div>
        <Link
          to="/"
          className="rounded-lg border border-surface-border px-3 py-2 text-sm text-slate-300 hover:border-slate-500"
        >
          Back to dashboard
        </Link>
      </div>

      <div className="rounded-xl border border-surface-border bg-surface-card p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Accuracy</p>
        <p className="mt-2 text-3xl font-semibold text-profit">{(ml.accuracy * 100).toFixed(2)}%</p>
      </div>

      <div className="rounded-xl border border-surface-border bg-surface-card">
        <div className="border-b border-surface-border px-4 py-3">
          <h3 className="text-sm font-semibold text-white">Classification report</h3>
          <p className="text-xs text-slate-500">sklearn.metrics.classification_report</p>
        </div>
        <pre className="max-h-[480px] overflow-auto whitespace-pre-wrap p-4 font-mono text-xs leading-relaxed text-slate-300">
          {ml.classification_report}
        </pre>
      </div>

      <div className="overflow-hidden rounded-xl border border-surface-border bg-surface-card">
        <div className="border-b border-surface-border px-4 py-3">
          <h3 className="text-sm font-semibold text-white">Predictions (test split)</h3>
          <p className="text-xs text-slate-500">
            Rows align with <code className="text-accent">X_test</code> from your training routine. Target{" "}
            <code className="text-accent">1</code> means next candle up per <code className="text-accent">
              prepare_ml_data
            </code>
            .
          </p>
        </div>
        <div className="max-h-[520px] overflow-auto">
          <table className="min-w-full divide-y divide-surface-border text-sm">
            <thead className="bg-surface sticky top-0 z-10">
              <tr className="text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                <th className="px-4 py-2">Timestamp</th>
                <th className="px-4 py-2">Actual</th>
                <th className="px-4 py-2">Predicted</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {ml.predictions.map((p, i) => (
                <tr key={`${p.timestamp}-${i}`} className="hover:bg-surface/80">
                  <td className="whitespace-nowrap px-4 py-2 font-mono text-xs text-slate-300">
                    {p.timestamp.replace("T", " ").slice(0, 19)}
                  </td>
                  <td className="px-4 py-2 font-mono text-xs text-slate-200">{p.actual}</td>
                  <td
                    className={`px-4 py-2 font-mono text-xs font-medium ${
                      p.actual === p.predicted ? "text-profit" : "text-loss"
                    }`}
                  >
                    {p.predicted}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
