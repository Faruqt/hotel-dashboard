/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        body: "#ffffff",
        light: "#f7f7f7",
        nav: "#3b3b3b",
        button: "#ff5757",
        overlay: "#bfb8b0",
        "input-bg": "#e5e7eb",
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
        merriweather: ['Merriweather', 'sans-serif'],
        karla: ['Karla', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
