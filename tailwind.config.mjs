/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        carbon: {
          950: '#070809',
          900: '#0b0d0e', // Base background
          850: '#0e1113', // Header / sub-base
          800: '#13171a', // Card / surface
          750: '#1a2024', // Elevated surface
          700: '#232a2e', // Border / line
          600: '#323b42', // Border hover
          500: '#48535c',
          400: '#86929d', // Muted text
          300: '#b0b8c1',
          100: '#e6edf3', // Primary text
        },
        amber: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b', // Primary Fastboot Amber
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
