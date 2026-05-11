import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/run_backtest": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/metrics": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/trades": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/signals": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/ml_results": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/health": { target: "http://127.0.0.1:8000", changeOrigin: true },
    },
  },
});
