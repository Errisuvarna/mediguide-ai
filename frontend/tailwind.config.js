/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff9ff', 100: '#dbf1ff', 200: '#bfe8ff', 300: '#93dbff',
          400: '#5fc4ff', 500: '#2ba8ff', 600: '#1487f0', 700: '#0f6cd6',
          800: '#1458ac', 900: '#164b87',
        },
        accent: { 500: '#14b8a6', 600: '#0d9488' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
