/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0f172a',        // Slate 900
        card: '#1e293b',        // Slate 800
        border: '#334155',      // Slate 700
        primary: '#6366f1',     // Indigo 500
        success: '#22c55e',     // Green 500
        warning: '#f59e0b',     // Amber 500
      }
    },
  },
  plugins: [],
}