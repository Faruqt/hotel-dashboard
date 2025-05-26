/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        body: "#ffffff",
        light: "#f7f7f7",
        dark: "#3b3b3b",
        button: "#ff5757",
        overlay: "#bfb8b0",
        input: "#e5e7eb",
      },
      animation: {
        "spin-slow": "spin 2s linear infinite",
      },
      fontFamily: {
        inter: ["Inter", "sans-serif"],
        merriweather: ["Merriweather", "sans-serif"],
        karla: ["Karla", "sans-serif"],
      },
    },
  },
  plugins: [],
};
