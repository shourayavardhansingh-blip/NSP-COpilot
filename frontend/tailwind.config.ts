import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bis: {
          navy: "#0a192f",
          dark: "#0f172a",
          card: "#1e293b",
          border: "#334155",
          accent: "#2563eb",
          accentLight: "#3b82f6",
          gold: "#eab308",
          emerald: "#10b981",
          amber: "#f59e0b",
          red: "#ef4444",
        }
      }
    },
  },
  plugins: [],
};
export default config;
