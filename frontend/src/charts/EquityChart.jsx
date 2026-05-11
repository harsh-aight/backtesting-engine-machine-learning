import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function formatTick(ts) {
  try {
    const d = new Date(ts);
    return `${d.getUTCMonth() + 1}/${d.getUTCDate()}`;
  } catch {
    return ts;
  }
}

export function EquityChart({ data }) {
  if (!data?.length) {
    return (
      <div className="flex h-72 items-center justify-center rounded-xl border border-dashed border-surface-border text-sm text-slate-500">
        Run a backtest to plot portfolio values.
      </div>
    );
  }

  return (
    <div className="h-80 w-full rounded-xl border border-surface-border bg-surface-card p-2 sm:p-4">
      <div className="mb-2 flex items-center justify-between px-1">
        <h2 className="text-sm font-semibold text-white">Equity curve</h2>
        <span className="text-xs text-slate-500">Portfolio value over time</span>
      </div>
      <ResponsiveContainer width="100%" height="88%">
        <AreaChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="equityFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#22c55e" stopOpacity={0.35} />
              <stop offset="100%" stopColor="#22c55e" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e2533" vertical={false} />
          <XAxis
            dataKey="timestamp"
            tickFormatter={formatTick}
            stroke="#64748b"
            tick={{ fontSize: 11 }}
            minTickGap={24}
          />
          <YAxis
            stroke="#64748b"
            tick={{ fontSize: 11 }}
            tickFormatter={(v) =>
              v >= 1_000_000 ? `${(v / 1_000_000).toFixed(1)}M` : v >= 1000 ? `${(v / 1000).toFixed(1)}k` : `${v}`
            }
            width={56}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "#12161f",
              border: "1px solid #1e2533",
              borderRadius: "0.5rem",
              fontSize: "12px",
            }}
            labelFormatter={(label) => new Date(label).toISOString().slice(0, 16).replace("T", " ")}
            formatter={(value) => [Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 }), "Value"]}
          />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#22c55e"
            strokeWidth={2}
            fill="url(#equityFill)"
            dot={false}
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
