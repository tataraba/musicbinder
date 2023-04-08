/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {

      /* Extend typography */
      fontFamily: {
        'livvic': ['Livvic', 'sans-serif'],
      },

      /* Extend available colors */
      colors: {
        primary: '#18956d',
        secondary: '#3180b1',
        turquoise: {
          '50':  '#eef5f4',
          '100': '#cdf0f2',
          '200': '#95e6e1',
          '300': '#5bcdbe',
          '400': '#22af95',
          '500': '#18956d',
          '600': '#167e55',
          '700': '#156144',
          '800': '#104333',
          '900': '#0c2927',
        },
      }
    },
  },
  plugins: [],
}
