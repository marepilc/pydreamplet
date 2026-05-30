<script setup lang="ts">
const route = useRoute()
const path = route.path === '' ? '/' : route.path
const colorMode = useColorMode()
const mobileNavigationOpen = ref(false)

const navigation = [
  {
    title: 'Getting started',
    icon: 'i-lucide-book-open',
    path: '/getting-started',
    children: [
      {
        title: 'Getting started',
        path: '/getting-started'
      },
      {
        title: 'Drawing basics',
        path: '/drawing-basics'
      },
      {
        title: 'Path basics',
        path: '/path-basics'
      },
      {
        title: 'Transform basics',
        path: '/transform-basics'
      },
      {
        title: 'Text basics',
        path: '/text-basics'
      }
    ]
  },
  {
    title: 'Reference',
    icon: 'i-lucide-library',
    path: '/reference',
    children: [
      {
        title: 'Reference overview',
        path: '/reference'
      }
    ]
  }
]

const topNavigation = [
  {
    title: 'Getting started',
    path: '/getting-started'
  },
  {
    title: 'Drawing basics',
    path: '/drawing-basics'
  },
  {
    title: 'Path basics',
    path: '/path-basics'
  },
  {
    title: 'Transform basics',
    path: '/transform-basics'
  },
  {
    title: 'Text basics',
    path: '/text-basics'
  },
  {
    title: 'Reference',
    path: '/reference'
  }
]

const { data: page } = await useAsyncData(`docs:${path}`, () => {
  return queryCollection('docs').path(path).first()
})

if (!page.value) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Page not found'
  })
}

useSeoMeta({
  title: page.value.title,
  description: page.value.description
})

const isDark = computed({
  get() {
    return colorMode.value === 'dark'
  },
  set(value) {
    colorMode.preference = value ? 'dark' : 'light'
  }
})
</script>

<template>
  <main class="min-h-screen bg-white text-neutral-950 dark:bg-neutral-950 dark:text-white">
    <header
      class="sticky top-0 z-10 border-b border-neutral-200 bg-white/85 backdrop-blur dark:border-neutral-800 dark:bg-neutral-950/85"
    >
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <div class="flex items-center gap-6">
          <NuxtLink to="/" class="flex items-center gap-2 text-sm font-semibold tracking-wide">
            <span class="flex size-8 items-center justify-center rounded-md bg-teal-700 dark:bg-teal-500">
              <img src="/brand/hummingbird.svg" alt="" class="h-5 w-5" aria-hidden="true">
            </span>
            <span>pyDreamplet</span>
          </NuxtLink>
          <nav class="hidden items-center gap-5 text-sm text-neutral-600 dark:text-neutral-300 md:flex">
            <NuxtLink
              v-for="item in topNavigation"
              :key="item.path"
              :to="item.path"
            >
              {{ item.title }}
            </NuxtLink>
          </nav>
        </div>

        <div class="flex items-center gap-1">
          <ClientOnly>
            <UButton
              :icon="isDark ? 'i-lucide-sun' : 'i-lucide-moon'"
              color="neutral"
              variant="ghost"
              :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
              @click="isDark = !isDark"
            />
            <template #fallback>
              <div class="size-8" />
            </template>
          </ClientOnly>

          <USlideover
            v-model:open="mobileNavigationOpen"
            side="left"
            title="Documentation"
            :ui="{ content: 'max-w-80' }"
          >
            <UButton
              icon="i-lucide-menu"
              color="neutral"
              variant="ghost"
              class="md:hidden"
              aria-label="Open documentation navigation"
            />

            <template #body>
              <UContentNavigation
                :navigation="navigation"
                type="single"
                default-open
                highlight
                color="neutral"
                variant="link"
                @click="mobileNavigationOpen = false"
              />
            </template>
          </USlideover>
        </div>
      </div>
    </header>

    <div class="mx-auto grid max-w-7xl grid-cols-1 gap-10 px-4 py-10 sm:px-6 lg:grid-cols-[220px_minmax(0,1fr)]">
      <UPageAside>
        <UContentNavigation
          :navigation="navigation"
          type="single"
          default-open
          highlight
          color="neutral"
          variant="link"
        />
      </UPageAside>

      <article class="docs-content max-w-3xl">
        <ContentRenderer :value="page" />
      </article>
    </div>
  </main>
</template>
