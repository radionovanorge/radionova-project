/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../tears/templates/**/*.html',
    '../tears/static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'radionova-maroon': {
          DEFAULT: '#590D1A',
          dark: '#450A14',
          light: '#701021',
        },
        'radionova-red': '#EB1F2A',
        'radionova-dark': '#1a0a0f',
        'radionova-light': '#f8f4f5',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/typography'),
  ],
} 