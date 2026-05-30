export default defineNuxtConfig({
  compatibilityDate: '2026-05-30',
  modules: ['@nuxt/content', '@nuxt/ui'],
  css: ['~/assets/css/main.css'],
  devtools: {
    enabled: false
  },
  ui: {
    fonts: false
  },
  app: {
    baseURL: process.env.NUXT_APP_BASE_URL || '/',
    head: {
      titleTemplate: '%s · pyDreamplet',
      htmlAttrs: {
        lang: 'en'
      },
      link: [
        { rel: 'icon', href: '/favicon.ico' }
      ]
    }
  },
  content: {
    experimental: {
      sqliteConnector: 'native'
    },
    build: {
      markdown: {
        toc: {
          depth: 3,
          searchDepth: 3
        }
      }
    }
  }
})
