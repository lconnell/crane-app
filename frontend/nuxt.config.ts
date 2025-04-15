import { defineNuxtConfig } from 'nuxt/config';

import vuetify from 'vite-plugin-vuetify';

export default defineNuxtConfig({
  modules: [
    // '@sidebase/nuxt-auth' removed. Use FastAPI for authentication.
  ],

  css: [
    'vuetify/styles',
  ],

  vite: {
    define: {
      'process.env.DEBUG': false,
    },
    plugins: [
      vuetify({
        autoImport: true,
      }),
    ],
  },

  // Removed invalid 'auth' property. Configure auth module via runtimeConfig or module options if needed.

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000/api',
    },
  },

  compatibilityDate: '2025-04-15',

  build: {
    transpile: ['vuetify', 'vite-plugin-vuetify'],
  },

});