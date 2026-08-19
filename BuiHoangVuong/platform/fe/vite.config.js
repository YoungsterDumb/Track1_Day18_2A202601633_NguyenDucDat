import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Dev server proxies /api to the backend; in the image nginx does the same.
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: { "/api": { target: process.env.VITE_API_TARGET || "http://be:8000", changeOrigin: true } },
  },
});
