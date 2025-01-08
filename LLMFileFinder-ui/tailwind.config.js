/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts,scss}",
  ],
  theme: {
    extend: {
      colors:{
        "primary": "rgb(7 89 133)",
      },
      keyframes: {
        "small-jump": {
          "0%": {transform: "scale(100%)"},
          "50%": {transform: "scale(110%)"},
          "100%": {transform: "scale(100%)"},
        }
      },
      animation: {
        "small-jump": "small-jump 1s ease-in-out",
      }
    },
  },
  plugins: [
    require('tailwindcss-animated')
  ],
}

