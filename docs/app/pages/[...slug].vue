<script setup lang="ts">
const route = useRoute()
const path = route.path === '' ? '/' : route.path
const colorMode = useColorMode()

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
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <div class="flex items-center gap-6">
          <NuxtLink to="/" class="flex items-center gap-2 text-sm font-semibold tracking-wide">
            <span class="flex size-8 items-center justify-center rounded-md bg-teal-700 dark:bg-teal-500">
              <img src="/brand/hummingbird.svg" alt="" class="h-5 w-5" aria-hidden="true">
            </span>
            <span>pyDreamplet</span>
          </NuxtLink>
          <nav class="hidden items-center gap-5 text-sm text-neutral-600 dark:text-neutral-300 md:flex">
            <NuxtLink to="/getting-started">Getting started</NuxtLink>
            <NuxtLink to="/reference">Reference</NuxtLink>
          </nav>
        </div>

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
      </div>
    </header>

    <div class="mx-auto grid max-w-7xl grid-cols-1 gap-10 px-6 py-10 lg:grid-cols-[220px_minmax(0,1fr)]">
      <aside class="hidden border-r border-neutral-200 pr-8 text-sm dark:border-neutral-800 lg:block">
        <nav class="sticky top-26 flex flex-col gap-2">
          <NuxtLink class="rounded-md px-3 py-2 font-medium text-neutral-950 dark:text-white" to="/">
            Documentation
          </NuxtLink>
          <NuxtLink class="rounded-md px-3 py-2 font-medium text-neutral-950 dark:text-white" to="/getting-started">
            Getting started
          </NuxtLink>
          <NuxtLink class="rounded-md px-3 py-2 font-medium text-neutral-950 dark:text-white" to="/reference">
            Reference
          </NuxtLink>
        </nav>
      </aside>

      <article class="docs-content max-w-3xl">
        <ContentRenderer :value="page" />
      </article>
    </div>
  </main>
</template>
