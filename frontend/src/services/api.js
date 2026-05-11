const base = import.meta.env.VITE_API_BASE ?? "";

async function parseError(res) {
  try {
    const body = await res.json();
    if (body?.detail) {
      return typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    }
  } catch {
    /* ignore */
  }
  return res.statusText || "Unknown error";
}

export async function runBacktest(payload) {
  const res = await fetch(`${base}/run_backtest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(await parseError(res));
  }
  return res.json();
}
