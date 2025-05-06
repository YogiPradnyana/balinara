/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}', './node_modules/flowbite/**/*.js'],
  theme: {
    extend: {},
  },
  plugins: [require('flowbite/plugin')],
}
