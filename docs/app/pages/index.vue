<script setup lang="ts">
const colorMode = useColorMode()

useSeoMeta({
  title: 'pyDreamplet',
  description: 'A Python toolkit for precise SVG graphics, creative coding, and custom data visualization.'
})

const isDark = computed({
  get() {
    return colorMode.value === 'dark'
  },
  set(value) {
    colorMode.preference = value ? 'dark' : 'light'
  }
})

const highlights = [
  {
    icon: 'i-lucide-shapes',
    title: 'SVG primitives',
    description: 'Compose circles, paths, text, groups, gradients, masks, and animation directly from Python.'
  },
  {
    icon: 'i-lucide-chart-no-axes-combined',
    title: 'Data to geometry',
    description: 'Use scales and generators to turn values into visual structure without hiding the SVG model.'
  },
  {
    icon: 'i-lucide-notebook-tabs',
    title: 'Script or notebook',
    description: 'Save clean SVG files from scripts or display work inline while exploring ideas in notebooks.'
  }
]
</script>

<template>
  <main class="min-h-screen bg-neutral-50 text-neutral-950 dark:bg-neutral-950 dark:text-white">
    <header class="border-b border-neutral-200 bg-white/85 backdrop-blur dark:border-neutral-800 dark:bg-neutral-950/85">
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <NuxtLink to="/" class="flex items-center gap-2 text-sm font-semibold tracking-wide">
          <HummingbirdLogo class="h-5 w-6 text-teal-700 dark:text-teal-300" />
          <span>pyDreamplet</span>
        </NuxtLink>

        <nav class="hidden items-center gap-6 text-sm text-neutral-600 dark:text-neutral-300 md:flex">
          <NuxtLink to="/getting-started">
            Getting started
          </NuxtLink>
          <NuxtLink to="/drawing-basics">
            Drawing basics
          </NuxtLink>
          <NuxtLink to="/reference">
            Reference
          </NuxtLink>
        </nav>

        <ClientOnly>
          <UButton
            :icon="isDark ? 'i-lucide-moon' : 'i-lucide-sun'"
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

    <section class="border-b border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-950">
      <div class="mx-auto grid min-h-[calc(100vh-4rem)] max-w-7xl items-center gap-10 px-6 py-12 lg:grid-cols-[0.92fr_1.08fr]">
        <div class="max-w-2xl">
          <img
            src="/brand/pyDreamplet_logo.png"
            alt="pyDreamplet"
            class="mb-8 h-auto w-full max-w-md"
          >
          <p class="mb-4 text-sm font-semibold uppercase tracking-[0.16em] text-teal-700 dark:text-teal-300">
            Python to precise SVG
          </p>
          <h1 class="max-w-lg text-2xl font-semibold leading-9 tracking-normal text-neutral-950 dark:text-white md:text-3xl md:leading-10">
            Build expressive vector graphics with code.
          </h1>
          <p class="mt-6 max-w-xl text-lg leading-8 text-neutral-600 dark:text-neutral-300">
            pyDreamplet gives you composable SVG elements, scales, generators, and creative helpers for custom visualizations that need more control than a charting preset.
          </p>

          <div class="mt-8 flex flex-wrap gap-3">
            <UButton to="/getting-started" icon="i-lucide-play" size="lg">
              Getting started
            </UButton>
            <UButton to="/reference" icon="i-lucide-book-open" color="neutral" variant="outline" size="lg">
              API reference
            </UButton>
          </div>

          <dl class="mt-10 grid max-w-lg grid-cols-3 gap-5 border-t border-neutral-200 pt-6 text-sm dark:border-neutral-800">
            <div>
              <dt class="text-neutral-500 dark:text-neutral-400">
                Output
              </dt>
              <dd class="mt-1 font-semibold">
                SVG
              </dd>
            </div>
            <div>
              <dt class="text-neutral-500 dark:text-neutral-400">
                Runtime
              </dt>
              <dd class="mt-1 font-semibold">
                Python 3.12+
              </dd>
            </div>
            <div>
              <dt class="text-neutral-500 dark:text-neutral-400">
                Workflow
              </dt>
              <dd class="mt-1 font-semibold">
                Scripts + notebooks
              </dd>
            </div>
          </dl>
        </div>

        <div class="relative">
          <div class="overflow-hidden rounded-lg border border-neutral-200 bg-neutral-100 shadow-sm dark:border-neutral-800 dark:bg-neutral-900">
            <div class="flex items-center justify-between border-b border-neutral-200 px-4 py-3 text-xs text-neutral-500 dark:border-neutral-800 dark:text-neutral-400">
              <span>supplier-quality.svg</span>
              <span>generated with pyDreamplet</span>
            </div>
            <div class="aspect-[1.18] bg-white p-4">
              <img
                :src="'/showcase/supplier-quality.svg'"
                alt="Supplier quality performance SVG visualization generated with pyDreamplet"
                class="h-full w-full object-contain"
              >
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-neutral-50 px-6 py-14 dark:bg-neutral-950">
      <div class="mx-auto grid max-w-7xl gap-6 md:grid-cols-3">
        <article
          v-for="item in highlights"
          :key="item.title"
          class="rounded-lg border border-neutral-200 bg-white p-6 dark:border-neutral-800 dark:bg-neutral-900"
        >
          <UIcon :name="item.icon" class="mb-5 size-6 text-teal-700 dark:text-teal-300" />
          <h2 class="text-base font-semibold">
            {{ item.title }}
          </h2>
          <p class="mt-3 text-sm leading-6 text-neutral-600 dark:text-neutral-300">
            {{ item.description }}
          </p>
        </article>
      </div>
    </section>
  </main>
</template>
