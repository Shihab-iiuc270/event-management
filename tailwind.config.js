/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",          // Project-level templates
    "./events/**/*.{html,js,py}",          // App: events
    "./users/**/*.{html,js,py}",           // App: users
    "./event_management/**/*.{html,js,py}",
    './static/js/**/*.js',
     // Your main config folder
     // Your main config folder
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
