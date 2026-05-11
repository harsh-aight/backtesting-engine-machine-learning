function signalLabel(v) {
  if (v === 1) return "Buy";
  if (v === -1) return "Sell";
  return "Hold";
}

function signalBadge(v) {
  if (v === 1) return "bg-emerald-500/15 text-emerald-400";
  if (v === -1) return "bg-rose-500/15 text-rose-400";
  return "bg-slate-600/40 text-slate-300";
}

export function SignalsTable({ signals }) {
  return (
    <div className="overflow-hidden rounded-xl border border-surface-border bg-surface-card">
      <div className="border-b border-surface-border px-4 py-3">
        <h2 className="text-sm font-semibold text-white">Signals</h2>
        <p className="text-xs text-slate-500">Indicator columns and discrete signal from your engine.</p>
      </div>
      <div className="max-h-[420px] overflow-auto">
        <table className="min-w-full divide-y divide-surface-border text-sm">
          <thead className="bg-surface sticky top-0 z-10">
            <tr className="text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
              <th className="px-4 py-2">Timestamp</th>
              <th className="px-4 py-2">Close</th>
              <th className="px-4 py-2">SMA20</th>
              <th className="px-4 py-2">SMA50</th>
              <th className="px-4 py-2">RSI</th>
              <th className="px-4 py-2">Signal</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-border">
            {signals?.length ? (
              signals.map((s, i) => (
                <tr key={`${s.timestamp}-${i}`} className="hover:bg-surface/80">
                  <td className="whitespace-nowrap px-4 py-2 font-mono text-xs text-slate-300">
                    {s.timestamp.replace("T", " ").slice(0, 19)}
                  </td>
                  <td className="px-4 py-2 font-mono text-xs text-slate-200">
                    {Number(s.close).toFixed(2)}
                  </td>
                  <td className="px-4 py-2 font-mono text-xs text-slate-200">
                    {Number(s.sma20).toFixed(2)}
                  </td>
                  <td className="px-4 py-2 font-mono text-xs text-slate-200">
                    {Number(s.sma50).toFixed(2)}
                  </td>
                  <td className="px-4 py-2 font-mono text-xs text-slate-200">
                    {Number(s.rsi).toFixed(2)}
                  </td>
                  <td className="px-4 py-2">
                    <span className={`rounded-md px-2 py-0.5 text-xs font-semibold ${signalBadge(s.signal)}`}>
                      {signalLabel(s.signal)}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-sm text-slate-500">
                  No signal rows yet. Run a backtest.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
