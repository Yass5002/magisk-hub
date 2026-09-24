/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#edfbf9',
          100: '#d4f5f0',
          200: '#adeae1',
          300: '#78d9cd',
          400: '#3ec1b3',
          500: '#01af9c', // Official Magisk Teal
          600: '#009a8a',
          700: '#017a6e',
          800: '#046158',
          900: '#07504a',
        },
        magisk: '#01af9c',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
