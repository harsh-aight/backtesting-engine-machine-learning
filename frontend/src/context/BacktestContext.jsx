import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { runBacktest } from "../services/api.js";

const BacktestContext = createContext(null);

const defaultForm = {
  strategy: "ml",
  startDate: "2026-03-01",
  endDate: "2026-03-26",
  initialBalance: 10000,
};

export function BacktestProvider({ children }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [strategy, setStrategy] = useState(defaultForm.strategy);
  const [startDate, setStartDate] = useState(defaultForm.startDate);
  const [endDate, setEndDate] = useState(defaultForm.endDate);
  const [initialBalance, setInitialBalance] = useState(defaultForm.initialBalance);

  const execute = useCallback(async () => {
    setLoading(true);
    setError(null);
    const payload = {
      strategy,
      start_date: startDate,
      end_date: endDate,
      initial_balance: initialBalance,
    };
    try {
      const data = await runBacktest(payload);
      setResult(data);
      return data;
    } catch (e) {
      setError(e.message || "Request failed");
      setResult(null);
      throw e;
    } finally {
      setLoading(false);
    }
  }, [strategy, startDate, endDate, initialBalance]);

  const value = useMemo(
    () => ({
      result,
      loading,
      error,
      execute,
      clearError: () => setError(null),
      strategy,
      setStrategy,
      startDate,
      setStartDate,
      endDate,
      setEndDate,
      initialBalance,
      setInitialBalance,
    }),
    [
      result,
      loading,
      error,
      execute,
      strategy,
      startDate,
      endDate,
      initialBalance,
    ]
  );

  return <BacktestContext.Provider value={value}>{children}</BacktestContext.Provider>;
}

export function useBacktest() {
  const ctx = useContext(BacktestContext);
  if (!ctx) {
    throw new Error("useBacktest must be used within BacktestProvider");
  }
  return ctx;
}
