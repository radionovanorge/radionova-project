/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../../**/templates/**/*.html',
    '../../**/static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'radionova-maroon': {
          DEFAULT: '#5D1A2D',
          'dark': '#4A1422',
          'light': '#6E2138',
        },
        'radionova-dark': '#1a0a0f',
        'radionova-light': '#f8f4f5',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
} 