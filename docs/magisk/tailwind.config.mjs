/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        carbon: {
          950: '#070809',
          900: '#0b0d0e',
          850: '#0e1113',
          800: '#13171a',
          750: '#1a2024',
          700: '#232a2e',
          600: '#323b42',
          500: '#48535c',
          400: '#86929d',
          300: '#b0b8c1',
          100: '#e6edf3',
        },
        amber: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        brand: {
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
        },
        magisk: '#f59e0b',
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
