export function MetricCard({ label, value, sub, highlight }) {
  return (
    <div className="rounded-xl border border-surface-border bg-surface-card p-4 shadow-sm">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">{label}</p>
      <p
        className={`mt-2 text-2xl font-semibold tracking-tight sm:text-3xl ${
          highlight === "profit"
            ? "text-profit"
            : highlight === "loss"
              ? "text-loss"
              : "text-white"
        }`}
      >
        {value}
      </p>
      {sub ? <p className="mt-1 text-xs text-slate-500">{sub}</p> : null}
    </div>
  );
}
