function profitClass(pct) {
  if (pct == null) return "text-slate-400";
  if (pct > 0) return "text-profit font-medium";
  if (pct < 0) return "text-loss font-medium";
  return "text-slate-300";
}

export function TradeTable({ trades }) {
  return (
    <div className="overflow-hidden rounded-xl border border-surface-border bg-surface-card">
      <div className="border-b border-surface-border px-4 py-3">
        <h2 className="text-sm font-semibold text-white">Trade history</h2>
        <p className="text-xs text-slate-500">Executions from your backtester output.</p>
      </div>
      <div className="max-h-[420px] overflow-auto">
        <table className="min-w-full divide-y divide-surface-border text-sm">
          <thead className="bg-surface sticky top-0 z-10">
            <tr className="text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
              <th className="px-4 py-2">Timestamp</th>
              <th className="px-4 py-2">Trade type</th>
              <th className="px-4 py-2">Price</th>
              <th className="px-4 py-2 text-right">Profit %</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-border">
            {trades?.length ? (
              trades.map((t, i) => (
                <tr key={`${t.timestamp}-${i}`} className="hover:bg-surface/80">
                  <td className="whitespace-nowrap px-4 py-2 font-mono text-xs text-slate-300">
                    {t.timestamp.replace("T", " ").slice(0, 19)}
                  </td>
                  <td className="px-4 py-2">
                    <span
                      className={`rounded-md px-2 py-0.5 text-xs font-semibold ${
                        t.type === "BUY"
                          ? "bg-emerald-500/15 text-emerald-400"
                          : "bg-rose-500/15 text-rose-400"
                      }`}
                    >
                      {t.type}
                    </span>
                  </td>
                  <td className="px-4 py-2 font-mono text-slate-200">
                    {Number(t.price).toLocaleString(undefined, { maximumFractionDigits: 2 })}
                  </td>
                  <td className={`px-4 py-2 text-right font-mono text-xs ${profitClass(t.profit_pct)}`}>
                    {t.profit_pct == null ? "—" : `${t.profit_pct.toFixed(2)}%`}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-sm text-slate-500">
                  No trades yet. Run a backtest.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
