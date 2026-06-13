<script setup lang="ts">
const siteUrl = useRuntimeConfig().public.siteUrl.replace(/\/+$/, '')
const showcaseRepository = 'https://github.com/marepilc/pydreamplet-showcase'

useSeoMeta({
  title: 'Gallery',
  description: 'Explore data visualizations, generative art, animations, and custom SVG graphics made with pyDreamplet and Python.',
  ogTitle: 'pyDreamplet Gallery',
  ogDescription: 'Data visualizations and creative coding projects made with Python and pyDreamplet.',
  ogType: 'website',
  ogUrl: `${siteUrl}/gallery`,
  ogImage: '/showcase/supplier_performance_chart_light.svg',
  twitterCard: 'summary_large_image',
  twitterTitle: 'pyDreamplet Gallery',
  twitterDescription: 'Explore data visualizations and creative coding projects made with Python.'
})

useHead({
  link: [
    {
      rel: 'canonical',
      href: `${siteUrl}/gallery`
    }
  ]
})

const categories = [
  { label: 'All work', value: 'all' },
  { label: 'Data visualization', value: 'data-visualization' },
  { label: 'Generative art', value: 'generative-art' },
  { label: 'Animation', value: 'animation' }
]

const projects = [
  {
    title: 'Supplier performance',
    description: 'A dashboard-style comparison of supplier quality, delivery, cost, and risk.',
    image: '/showcase/supplier_performance_chart_light.svg',
    darkImage: '/showcase/supplier_performance_chart_dark.svg',
    alt: 'Supplier performance chart made with pyDreamplet',
    category: 'data-visualization',
    categoryLabel: 'Data visualization',
    tags: ['scales', 'labels', 'custom chart'],
    source: 'supplier_performance.py'
  },
  {
    title: 'Polar noise',
    description: 'Layered contours generated from polar vectors and repeatable simplex noise.',
    image: '/showcase/polar_noise.svg',
    darkImage: '/showcase/polar_noise.svg',
    alt: 'Polar noise generative artwork made with pyDreamplet',
    category: 'generative-art',
    categoryLabel: 'Generative art',
    tags: ['simplex noise', 'paths', 'morphing'],
    source: 'polar_noise.py'
  },
  {
    title: 'Alice word cloud',
    description: 'A word cloud generated from Alice in Wonderland with measured typography and data-driven placement.',
    image: '/showcase/alice_word_cloud_light.svg',
    darkImage: '/showcase/alice_word_cloud_dark.svg',
    alt: 'Alice in Wonderland word cloud made with pyDreamplet',
    category: 'data-visualization',
    categoryLabel: 'Data visualization',
    tags: ['typography', 'layout', 'text data'],
    source: 'alice_word_cloud.py'
  },
  {
    title: 'Soap bubble',
    description: 'A translucent animated illustration composed with gradients, filters, and clipping.',
    image: '/showcase/soap_bubble_light.svg',
    darkImage: '/showcase/soap_bubble_dark.svg',
    alt: 'Animated soap bubble illustration made with pyDreamplet',
    category: 'animation',
    categoryLabel: 'Animation',
    tags: ['filters', 'gradients', 'clipping'],
    source: 'soap_bubble.py'
  },
  {
    title: 'Dancing circles',
    description: 'An animated radial composition built from grouped circles and blended strokes.',
    image: '/showcase/dancing_circles_light.svg',
    darkImage: '/showcase/dancing_circles_dark.svg',
    alt: 'Dancing circles animation made with pyDreamplet',
    category: 'animation',
    categoryLabel: 'Animation',
    tags: ['animation', 'groups', 'color'],
    source: 'dancing_circles.py'
  },
  {
    title: 'Multi-series line chart',
    description: 'A compact chart with generated data, scales, markers, labels, and grid lines.',
    image: '/showcase/tutorial_line_chart_final.svg',
    darkImage: '/showcase/tutorial_line_chart_final.svg',
    alt: 'Multi-series line chart made with pyDreamplet',
    category: 'data-visualization',
    categoryLabel: 'Data visualization',
    tags: ['scales', 'markers', 'lines'],
    source: 'line_chart.py'
  },
  {
    title: 'Waffle chart',
    description: 'A direct visual comparison of proportions using a precise ten-by-ten grid.',
    image: '/showcase/tutorial_waffle_chart.svg',
    darkImage: '/showcase/tutorial_waffle_chart.svg',
    alt: 'Waffle chart made with pyDreamplet',
    category: 'data-visualization',
    categoryLabel: 'Data visualization',
    tags: ['proportions', 'grid', 'color'],
    source: 'waffle_chart.py'
  },
  {
    title: 'Creative coding study',
    description: 'An expressive procedural graphic exploring repeated geometry and SVG color.',
    image: '/showcase/creative-coding.svg',
    darkImage: '/showcase/creative-coding.svg',
    alt: 'Creative coding study made with Python and pyDreamplet',
    category: 'generative-art',
    categoryLabel: 'Generative art',
    tags: ['procedural', 'geometry', 'color'],
    source: 'creative_coding_study.py'
  }
]

const activeCategory = ref('all')
const visibleProjects = computed(() => {
  if (activeCategory.value === 'all') {
    return projects
  }

  return projects.filter(project => project.category === activeCategory.value)
})

const sourceUrl = (source: string) => `${showcaseRepository}/blob/master/scripts/${source}`
</script>

<template>
  <main class="min-h-screen bg-neutral-50 text-neutral-950 dark:bg-neutral-950 dark:text-white">
    <header class="sticky top-0 z-10 border-b border-neutral-200 bg-white/85 backdrop-blur dark:border-neutral-800 dark:bg-neutral-950/85">
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <div class="flex items-center gap-6">
          <NuxtLink to="/" class="flex items-center gap-2 text-sm font-semibold tracking-wide">
            <HummingbirdLogo class="h-5 w-6 text-teal-700 dark:text-teal-300" />
            <span>pyDreamplet</span>
          </NuxtLink>
          <nav class="hidden items-center gap-5 text-sm text-neutral-600 dark:text-neutral-300 md:flex">
            <NuxtLink to="/getting-started">Getting started</NuxtLink>
            <NuxtLink to="/gallery" class="font-semibold text-neutral-950 dark:text-white">Gallery</NuxtLink>
            <NuxtLink to="/tutorials">Tutorials</NuxtLink>
            <NuxtLink to="/reference">Reference</NuxtLink>
          </nav>
        </div>

        <div class="flex items-center gap-1">
          <SearchButton />
          <UButton
            :to="showcaseRepository"
            target="_blank"
            rel="noopener noreferrer"
            icon="i-lucide-github"
            color="neutral"
            variant="ghost"
            aria-label="Open the pyDreamplet showcase repository"
          />
          <ThemeToggle />
        </div>
      </div>
    </header>

    <section class="border-b border-neutral-200 bg-white px-6 py-16 dark:border-neutral-800 dark:bg-neutral-950">
      <div class="mx-auto max-w-7xl">
        <p class="text-sm font-semibold uppercase tracking-[0.16em] text-teal-700 dark:text-teal-300">
          Made with Python
        </p>
        <div class="mt-4 grid gap-6 lg:grid-cols-[1fr_0.7fr] lg:items-end">
          <h1 class="max-w-3xl text-4xl font-semibold leading-tight tracking-tight md:text-5xl">
            Data visualization meets creative coding.
          </h1>
          <p class="max-w-xl text-base leading-7 text-neutral-600 dark:text-neutral-300">
            Explore complete graphics made with pyDreamplet. Every project links to runnable Python source code you can study, adapt, and build on.
          </p>
        </div>
      </div>
    </section>

    <section class="px-6 py-12">
      <div class="mx-auto max-w-7xl">
        <div class="mb-8 flex flex-wrap gap-2" aria-label="Filter gallery projects">
          <button
            v-for="category in categories"
            :key="category.value"
            type="button"
            class="rounded-full border px-4 py-2 text-sm font-medium transition-colors"
            :class="activeCategory === category.value
              ? 'border-teal-700 bg-teal-700 text-white dark:border-teal-300 dark:bg-teal-300 dark:text-neutral-950'
              : 'border-neutral-300 bg-white text-neutral-700 hover:border-neutral-500 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-300 dark:hover:border-neutral-500'"
            :aria-pressed="activeCategory === category.value"
            @click="activeCategory = category.value"
          >
            {{ category.label }}
          </button>
        </div>

        <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="project in visibleProjects"
            :key="project.source"
            class="group overflow-hidden rounded-xl border border-neutral-200 bg-white transition hover:-translate-y-1 hover:shadow-lg dark:border-neutral-800 dark:bg-neutral-900"
          >
            <div class="aspect-[4/3] overflow-hidden border-b border-neutral-200 bg-neutral-100 p-5 dark:border-neutral-800 dark:bg-neutral-950">
              <img
                v-if="project.image"
                :src="project.image"
                :alt="project.alt"
                width="900"
                height="675"
                loading="lazy"
                decoding="async"
                class="h-full w-full object-contain transition duration-300 group-hover:scale-[1.03] dark:hidden"
              >
              <img
                v-if="project.darkImage"
                :src="project.darkImage"
                :alt="project.alt"
                width="900"
                height="675"
                loading="lazy"
                decoding="async"
                class="hidden h-full w-full object-contain transition duration-300 group-hover:scale-[1.03] dark:block"
              >
              <div
                v-if="!project.image"
                class="flex h-full flex-col items-center justify-center text-center text-neutral-500 dark:text-neutral-400"
              >
                <UIcon name="i-lucide-cloud" class="size-10 text-teal-700 dark:text-teal-300" />
                <span class="mt-3 text-sm font-semibold">Preview coming soon</span>
              </div>
            </div>

            <div class="p-5">
              <p class="text-xs font-semibold uppercase tracking-[0.14em] text-teal-700 dark:text-teal-300">
                {{ project.categoryLabel }}
              </p>
              <h2 class="mt-2 text-lg font-semibold">
                {{ project.title }}
              </h2>
              <p class="mt-3 min-h-18 text-sm leading-6 text-neutral-600 dark:text-neutral-300">
                {{ project.description }}
              </p>
              <ul class="mt-4 flex flex-wrap gap-2" aria-label="Techniques used">
                <li
                  v-for="tag in project.tags"
                  :key="tag"
                  class="rounded bg-neutral-100 px-2 py-1 text-xs text-neutral-600 dark:bg-neutral-800 dark:text-neutral-300"
                >
                  {{ tag }}
                </li>
              </ul>
              <UButton
                :to="sourceUrl(project.source)"
                target="_blank"
                rel="noopener noreferrer"
                icon="i-lucide-code-xml"
                trailing-icon="i-lucide-external-link"
                color="neutral"
                variant="outline"
                class="mt-5"
              >
                View source
              </UButton>
            </div>
          </article>
        </div>

        <div class="mt-14 flex flex-col gap-5 rounded-xl border border-neutral-200 bg-white p-7 text-neutral-950 sm:flex-row sm:items-center sm:justify-between dark:border-neutral-800 dark:bg-neutral-900 dark:text-white">
          <div>
            <h2 class="text-xl font-semibold">Explore the complete showcase</h2>
            <p class="mt-2 text-sm leading-6 text-neutral-600 dark:text-neutral-300">
              Clone the repository to run the examples and experiment with their source code.
            </p>
          </div>
          <UButton
            :to="showcaseRepository"
            target="_blank"
            rel="noopener noreferrer"
            icon="i-lucide-github"
            size="lg"
            class="bg-teal-700 text-white hover:bg-teal-800 active:bg-teal-900 focus-visible:ring-teal-700 dark:bg-teal-300 dark:text-neutral-950 dark:hover:bg-teal-200 dark:active:bg-teal-100 dark:focus-visible:ring-teal-300"
          >
            Open on GitHub
          </UButton>
        </div>
      </div>
    </section>
  </main>
</template>
