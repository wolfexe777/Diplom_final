module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}

const colors = require('tailwindcss/colors')

module.exports = {
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: colors.black,
      white: colors.white,
      gray: colors.gray,
      emerald: colors.emerald,
      indigo: colors.indigo,
      yellow: colors.yellow,
      orange:colors.orange,
      cyan:colors.cyan,
      violet:colors.violet,
      purple:colors.purple,
      pink:colors.pink,
      sky:colors.sky,
      teal:colors.teal
      fuchsia:colors.fuchsia
    },
  },
}