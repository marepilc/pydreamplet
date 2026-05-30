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
        { rel: 'icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Proza+Libre:wght@400;500;600;700&display=swap'
        }
      ]
    }
  },
  content: {
    experimental: {
      sqliteConnector: 'native'
    },
    build: {
      markdown: {
        highlight: {
          theme: {
            default: 'github-light-high-contrast',
            dark: 'github-dark'
          },
          langs: [
            'js',
            'jsx',
            'json',
            'ts',
            'tsx',
            'vue',
            'css',
            'html',
            'bash',
            'shell',
            'console',
            'python',
            'md',
            'mdc',
            'yaml',
            'xml'
          ]
        },
        toc: {
          depth: 3,
          searchDepth: 3
        }
      }
    }
  }
})
