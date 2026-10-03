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
        background: "#0B1020",
        surface: {
          primary: "#111827",
          secondary: "#172033",
          tertiary: "#1E293B",
        },
        border: {
          subtle: "#1F293D",
          DEFAULT: "#263247",
          focus: "#3B82F6",
        },
        text: {
          primary: "#F8FAFC",
          secondary: "#A8B3C2",
          muted: "#64748B",
        },
        accent: {
          DEFAULT: "#1877F2",
          hover: "#1565C0",
        },
        status: {
          success: "#10B981",
          warning: "#F59E0B",
          danger: "#EF4444",
          info: "#6366F1",
        },
      },
    },
  },
  plugins: [],
};

export default config;
