import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "var(--color-background)",
        surface: "var(--color-surface)",
        muted: "var(--color-muted)",
        text: "var(--color-text)",
        subdued: "var(--color-subdued)",
        border: "var(--color-border)",
        primary: "var(--color-primary)",
        accent: "var(--color-accent)",
        success: "var(--color-success)",
        danger: "var(--color-danger)",
        hero: "var(--color-hero)",
        "soft-blue": "var(--color-soft-blue)",
        auth: "var(--color-auth)",
        "auth-dark": "var(--color-auth-dark)"
      },
      borderRadius: {
        app: "8px"
      },
      boxShadow: {
        soft: "0 10px 30px color-mix(in oklab, var(--color-text) 9%, transparent)"
      }
    }
  },
  plugins: []
} satisfies Config;
