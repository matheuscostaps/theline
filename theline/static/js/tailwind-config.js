// static/js/tailwind-config.js
tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: '#faf7fd',
        secundary: '#8e34e2',

        background: '#f3f1f5',
        secundaryBackground: '#f0eef5',

        white: '#ffffff',
        white2: '#fbf8fd',

        gray: '#2c2c2c',
        gray2: '#5e5e5e',

        itemHover: '#822fcf10',

        divisorBorder: '#e0e0e0',

        red: '#ee2460',
        blue: '#2e9efa',
      },
      fontFamily: {
        sans: ['Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif'],
      }
    }
  },
  plugins: [
    function ({ addComponents }) {
      addComponents({
        '.menu-link': {
          color: '#3b3b3b',
          fontSize: '16px',
          textDecoration: 'none',
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '8px 20px',
          borderRadius: '8px',
          fontWeight: '400',
          transition: 'background-color 0.3s ease, color 0.3s ease',

          '&:hover': {
            color: '#822fcf',
            backgroundColor: '#822fcf40',
            textDecoration: 'underline',
          },

          'svg': {
            width: '16px',
            height: '16px',
            flexShrink: '0',
            display: 'block',
            fill: 'currentColor',

            'path': {
              fill: 'currentColor',
            }
          }
        },
        '.menu-link-active': {
          color: '#822fcf !important',
          backgroundColor: '#822fcf10',
          fontWeight: '600',
        }
      })
    }
  ]
}