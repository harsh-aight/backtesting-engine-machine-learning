import { Outlet } from "react-router-dom";
import { useBacktest } from "../context/BacktestContext.jsx";
import { TopNav } from "./TopNav.jsx";

export function AppShell() {
  const {
    strategy,
    setStrategy,
    execute,
    loading,
    startDate,
    setStartDate,
    endDate,
    setEndDate,
    initialBalance,
    setInitialBalance,
  } = useBacktest();

  return (
    <div className="flex min-h-full flex-col bg-surface">
      <TopNav
        strategy={strategy}
        onStrategyChange={setStrategy}
        onRun={() => execute()}
        loading={loading}
        startDate={startDate}
        endDate={endDate}
        initialBalance={initialBalance}
        onStartChange={setStartDate}
        onEndChange={setEndDate}
        onBalanceChange={setInitialBalance}
      />
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-6 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  );
}
