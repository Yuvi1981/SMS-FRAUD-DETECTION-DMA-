/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        droit: {
          bg: '#E8E7EC',
          canvas: '#FCFCFE',
          sidebar: '#2B2257',
          sidebarDark: '#201844',
          sidebarActive: '#3F3572',
          sidebarHover: '#352B66',
          purple: '#6045F5',
          purpleHover: '#5035E0',
          purpleLight: '#EDE9FE',
          purpleBar: '#5A43F5',
          purpleBarPale: '#D8D8F6',
          bluePastel: '#DDE6FF',
          blueAreaFill: '#EAF0FF',
          pinkPastel: '#F9E1E4',
          mintPastel: '#DCEFEB',
          textDark: '#19153F',
          textMuted: '#77778D',
          border: '#E6E6EF',
          badgeRed: '#EB5757',
          badgeGreen: '#27AE60',
          badgeOrange: '#F2994A'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        'card': '12px',
        'subtle': '10px'
      },
      boxShadow: {
        'card': '0 2px 8px -1px rgba(25, 21, 63, 0.04), 0 1px 3px rgba(25, 21, 63, 0.02)',
        'elevated': '0 12px 28px -4px rgba(25, 21, 63, 0.06), 0 4px 12px -2px rgba(25, 21, 63, 0.03)',
        'dropdown': '0 12px 30px rgba(25, 21, 63, 0.12)'
      }
    },
  },
  plugins: [],
}
