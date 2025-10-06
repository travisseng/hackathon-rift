/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // League of Legends inspired colors
        'lol-gold': {
          DEFAULT: '#C89B3C',
          light: '#F0E6D2',
          dark: '#937341',
        },
        'lol-blue': {
          DEFAULT: '#0AC8B9',
          light: '#58D3C8',
          dark: '#0397AB',
        },
        'lol-dark': {
          DEFAULT: '#010A13',
          light: '#1E2328',
          lighter: '#31313C',
        },
      },
      backgroundImage: {
        'rift-pattern': "url('/assets/rift-bg.png')",
      },
      animation: {
        'card-flip': 'flip 0.6s ease-in-out',
        'card-entrance': 'entrance 0.5s ease-out',
      },
      keyframes: {
        flip: {
          '0%': { transform: 'rotateY(0deg)' },
          '100%': { transform: 'rotateY(180deg)' },
        },
        entrance: {
          '0%': { opacity: '0', transform: 'translateY(20px) scale(0.95)' },
          '100%': { opacity: '1', transform: 'translateY(0) scale(1)' },
        },
      },
    },
  },
  plugins: [],
}
