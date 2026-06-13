<script setup lang="ts">
const siteUrl = useRuntimeConfig().public.siteUrl.replace(/\/+$/, '')

useSeoMeta({
  title: 'Advanced Charts and Creative Coding with Python',
  description: 'Build advanced charts, custom SVG visualizations, and creative coding graphics with Python. pyDreamplet gives you composable SVG elements, scales, generators, and precise export control.',
  ogTitle: 'pyDreamplet - Advanced Charts and Creative Coding with Python',
  ogDescription: 'A Python toolkit for advanced charts, custom SVG visualizations, generative graphics, and creative coding workflows.',
  ogType: 'website',
  ogUrl: siteUrl,
  ogImage: '/showcase/supplier_performance_chart_light.svg',
  twitterCard: 'summary_large_image',
  twitterTitle: 'pyDreamplet - Advanced Charts and Creative Coding with Python',
  twitterDescription: 'Build advanced charts and creative coding graphics with Python and export clean SVG.'
})

useHead({
  link: [
    {
      rel: 'canonical',
      href: siteUrl
    }
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'SoftwareApplication',
        name: 'pyDreamplet',
        applicationCategory: 'DeveloperApplication',
        operatingSystem: 'Windows, macOS, Linux',
        programmingLanguage: 'Python',
        description: 'A Python toolkit for advanced charts, custom SVG visualization, and creative coding.',
        keywords: [
          'advanced charts with Python',
          'creative coding with Python',
          'Python SVG library',
          'custom data visualization',
          'generative graphics'
        ],
        offers: {
          '@type': 'Offer',
          price: '0',
          priceCurrency: 'USD'
        }
      })
    },
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        name: 'pyDreamplet',
        url: siteUrl
      })
    }
  ]
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

const useCases = [
  {
    title: 'Advanced charts with Python',
    description: 'Create charts that need custom annotations, unusual geometry, precise labels, reusable markers, and SVG output that remains editable after export.',
    link: '/tutorials/line-chart',
    linkLabel: 'Build a line chart'
  },
  {
    title: 'Creative coding with Python',
    description: 'Generate procedural layouts, organic shapes, noise-driven points, radial compositions, and layered SVG artwork from repeatable Python scripts.',
    link: '/tutorials/layered-svg-art',
    linkLabel: 'Explore layered SVG art'
  },
  {
    title: 'Scripted SVG production',
    description: 'Use Python to produce consistent technical illustrations, diagrams, reports, notebook visuals, and publication-ready vector assets.',
    link: '/reference',
    linkLabel: 'Browse the API'
  }
]

const capabilities = [
  'SVG elements with dynamic attributes and typed geometry helpers',
  'Scales, path generators, arcs, rings, splines, and symbols',
  'Text measurement, markers, masks, clip paths, gradients, and filters',
  'Collision helpers for labels and dense infographic layouts',
  'Notebook display and clean SVG file export'
]

const faqs = [
  {
    question: 'Can pyDreamplet build advanced charts with Python?',
    answer: 'Yes. pyDreamplet includes scales, path generators, shape helpers, markers, text tools, and low-level SVG access for charts that need more control than a preset charting library.'
  },
  {
    question: 'Is pyDreamplet useful for creative coding with Python?',
    answer: 'Yes. It includes point generators, noise helpers, organic shape helpers, SVG paths, gradients, masks, and animation primitives for procedural and generative graphics.'
  },
  {
    question: 'Does pyDreamplet export real SVG?',
    answer: 'Yes. pyDreamplet writes standard SVG markup, so generated graphics can be edited, embedded, versioned, or used in documentation and publishing workflows.'
  }
]

const showcaseSlides = [
  {
    title: 'Supplier performance chart',
    description: 'A dense SVG dashboard-style chart generated from Python.',
    light: '/showcase/supplier_performance_chart_light.svg',
    dark: '/showcase/supplier_performance_chart_dark.svg',
    alt: 'Supplier performance chart generated with pyDreamplet'
  },
  {
    title: 'Soap bubble illustration',
    description: 'A subtly animated soap bubble built with SVG filters and clipping.',
    light: '/showcase/soap_bubble_light.svg',
    dark: '/showcase/soap_bubble_dark.svg',
    alt: 'Soap bubble illustration generated with pyDreamplet'
  },
  {
    title: 'Dancing circles',
    description: 'An animated radial SVG composition using theme colors and blended strokes.',
    light: '/showcase/dancing_circles_light.svg',
    dark: '/showcase/dancing_circles_dark.svg',
    alt: 'Dancing circles animation generated with pyDreamplet'
  },
  {
    title: 'Polar noise',
    description: 'Layered animated contours shaped by polar vectors and simplex noise.',
    light: '/showcase/polar_noise.svg',
    dark: '/showcase/polar_noise.svg',
    alt: 'Polar noise animation generated with pyDreamplet'
  }
]

const featuredGallery = [
  {
    title: 'Supplier performance',
    category: 'Data visualization',
    image: '/showcase/supplier_performance_chart_light.svg',
    darkImage: '/showcase/supplier_performance_chart_dark.svg',
    alt: 'Supplier performance chart made with pyDreamplet'
  },
  {
    title: 'Polar noise',
    category: 'Generative art',
    image: '/showcase/polar_noise.svg',
    darkImage: '/showcase/polar_noise.svg',
    alt: 'Polar noise generative artwork made with pyDreamplet'
  },
  {
    title: 'Dancing circles',
    category: 'Animation',
    image: '/showcase/dancing_circles_light.svg',
    darkImage: '/showcase/dancing_circles_dark.svg',
    alt: 'Dancing circles animation made with pyDreamplet'
  }
]

const activeSlide = ref(0)
const currentSlide = computed(() => showcaseSlides[activeSlide.value])
let carouselTimer: ReturnType<typeof setInterval> | undefined

const goToSlide = (index: number) => {
  activeSlide.value = index
}

const nextSlide = () => {
  activeSlide.value = (activeSlide.value + 1) % showcaseSlides.length
}

const previousSlide = () => {
  activeSlide.value = (activeSlide.value + showcaseSlides.length - 1) % showcaseSlides.length
}

onMounted(() => {
  carouselTimer = setInterval(nextSlide, 7000)
})

onBeforeUnmount(() => {
  if (carouselTimer) {
    clearInterval(carouselTimer)
  }
})
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
          <NuxtLink to="/gallery">
            Gallery
          </NuxtLink>
          <NuxtLink to="/tutorials">
            Tutorials
          </NuxtLink>
          <NuxtLink to="/reference">
            Reference
          </NuxtLink>
        </nav>

        <div class="flex items-center gap-1">
          <SearchButton />
          <UButton
            to="https://github.com/marepilc/pydreamplet"
            target="_blank"
            rel="noopener noreferrer"
            icon="i-lucide-github"
            color="neutral"
            variant="ghost"
            aria-label="Open pyDreamplet on GitHub"
          />
          <ThemeToggle />
        </div>
      </div>
    </header>

    <section class="border-b border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-950">
      <div class="mx-auto grid max-w-7xl items-center gap-8 px-6 py-8 md:py-10 lg:grid-cols-[0.92fr_1.08fr]">
        <div class="max-w-2xl">
          <img
            src="/brand/pyDreamplet_logo.png"
            alt="pyDreamplet"
            class="mb-6 h-auto w-full max-w-md"
          >
          <p class="mb-4 text-sm font-semibold uppercase tracking-[0.16em] text-teal-700 dark:text-teal-300">
            Python to precise SVG
          </p>
          <h1 class="max-w-lg text-2xl font-semibold leading-9 tracking-normal text-neutral-950 dark:text-white md:text-3xl md:leading-10">
            Advanced charts and creative coding with Python.
          </h1>
          <p class="mt-5 max-w-xl text-lg leading-8 text-neutral-600 dark:text-neutral-300">
            pyDreamplet gives you composable SVG elements, scales, generators, and creative helpers for custom visualizations that need more control than a charting preset.
          </p>

          <div class="mt-7 flex flex-wrap gap-3">
            <UButton
              to="/getting-started"
              icon="i-lucide-play"
              size="lg"
              class="bg-teal-700 text-white hover:bg-teal-800 active:bg-teal-900 focus-visible:ring-teal-700 dark:bg-teal-300 dark:text-neutral-950 dark:hover:bg-teal-200 dark:active:bg-teal-100 dark:focus-visible:ring-teal-300"
            >
              Getting started
            </UButton>
            <UButton to="/tutorials" icon="i-lucide-graduation-cap" color="neutral" variant="outline" size="lg">
              Tutorials
            </UButton>
            <UButton to="/gallery" icon="i-lucide-images" color="neutral" variant="outline" size="lg">
              Gallery
            </UButton>
            <UButton to="/reference" icon="i-lucide-book-open" color="neutral" variant="outline" size="lg">
              API reference
            </UButton>
          </div>

          <dl class="mt-8 grid max-w-lg grid-cols-3 gap-5 border-t border-neutral-200 pt-5 text-sm dark:border-neutral-800">
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
                Charts + art
              </dd>
            </div>
          </dl>
        </div>

        <div class="relative">
          <div class="relative aspect-[1.18] overflow-hidden">
            <div
              v-for="(slide, index) in showcaseSlides"
              :key="slide.title"
              class="absolute inset-0 transition-opacity duration-500"
              :class="index === activeSlide ? 'opacity-100' : 'pointer-events-none opacity-0'"
              :aria-hidden="index !== activeSlide"
            >
              <img
                :src="slide.light"
                :alt="slide.alt"
                width="1500"
                height="1500"
                decoding="async"
                :fetchpriority="index === 0 ? 'high' : 'auto'"
                class="h-full w-full object-contain dark:hidden"
              >
              <img
                :src="slide.dark"
                :alt="slide.alt"
                width="1500"
                height="1500"
                decoding="async"
                class="hidden h-full w-full object-contain dark:block"
              >
            </div>
          </div>

          <div class="mt-4 flex items-center justify-between gap-4">
            <div class="min-w-0">
              <p class="truncate text-sm font-semibold text-neutral-950 dark:text-white">
                {{ currentSlide.title }}
              </p>
              <p class="mt-1 min-h-12 line-clamp-2 text-sm leading-6 text-neutral-600 dark:text-neutral-300">
                {{ currentSlide.description }}
              </p>
            </div>

            <div class="flex shrink-0 items-center gap-2">
              <UButton
                icon="i-lucide-chevron-left"
                color="neutral"
                variant="outline"
                size="sm"
                aria-label="Previous showcase image"
                @click="previousSlide"
              />
              <UButton
                icon="i-lucide-chevron-right"
                color="neutral"
                variant="outline"
                size="sm"
                aria-label="Next showcase image"
                @click="nextSlide"
              />
            </div>
          </div>

          <div class="mt-4 flex gap-2" aria-label="Showcase slides">
            <button
              v-for="(slide, index) in showcaseSlides"
              :key="slide.title"
              type="button"
              class="h-2.5 rounded-full transition-all focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700 dark:focus-visible:outline-teal-300"
              :class="index === activeSlide ? 'w-8 bg-teal-700 dark:bg-teal-300' : 'w-2.5 bg-neutral-300 hover:bg-neutral-400 dark:bg-neutral-700 dark:hover:bg-neutral-600'"
              :aria-label="`Show ${slide.title}`"
              :aria-current="index === activeSlide ? 'true' : undefined"
              @click="goToSlide(index)"
            />
          </div>
        </div>
      </div>
    </section>

    <section class="border-y border-neutral-200 bg-white px-6 py-14 dark:border-neutral-800 dark:bg-neutral-950">
      <div class="mx-auto max-w-7xl">
        <div class="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p class="text-sm font-semibold uppercase tracking-[0.16em] text-teal-700 dark:text-teal-300">
              Gallery
            </p>
            <h2 class="mt-3 text-2xl font-semibold leading-9 text-neutral-950 dark:text-white">
              See what Python can draw.
            </h2>
            <p class="mt-3 max-w-2xl text-base leading-7 text-neutral-600 dark:text-neutral-300">
              Explore data visualizations and generative graphics, then open the complete source code behind each project.
            </p>
          </div>
          <UButton to="/gallery" trailing-icon="i-lucide-arrow-right" color="neutral" variant="outline">
            Explore the gallery
          </UButton>
        </div>

        <div class="mt-8 grid gap-5 md:grid-cols-3">
          <NuxtLink
            v-for="project in featuredGallery"
            :key="project.title"
            to="/gallery"
            class="group overflow-hidden rounded-lg border border-neutral-200 bg-neutral-50 transition hover:-translate-y-1 hover:shadow-md dark:border-neutral-800 dark:bg-neutral-900"
          >
            <div class="aspect-[4/3] overflow-hidden border-b border-neutral-200 p-4 dark:border-neutral-800">
              <img
                :src="project.image"
                :alt="project.alt"
                width="720"
                height="540"
                loading="lazy"
                class="h-full w-full object-contain transition duration-300 group-hover:scale-[1.03] dark:hidden"
              >
              <img
                :src="project.darkImage"
                :alt="project.alt"
                width="720"
                height="540"
                loading="lazy"
                class="hidden h-full w-full object-contain transition duration-300 group-hover:scale-[1.03] dark:block"
              >
            </div>
            <div class="p-4">
              <p class="text-xs font-semibold uppercase tracking-[0.12em] text-teal-700 dark:text-teal-300">
                {{ project.category }}
              </p>
              <h3 class="mt-2 font-semibold">{{ project.title }}</h3>
            </div>
          </NuxtLink>
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

    <section class="border-y border-neutral-200 bg-white px-6 py-14 dark:border-neutral-800 dark:bg-neutral-950">
      <div class="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[0.8fr_1.2fr]">
        <div>
          <p class="text-sm font-semibold uppercase tracking-[0.16em] text-teal-700 dark:text-teal-300">
            Python visualization toolkit
          </p>
          <h2 class="mt-4 max-w-md text-2xl font-semibold leading-9 text-neutral-950 dark:text-white">
            Build the chart or graphic your project actually needs.
          </h2>
          <p class="mt-5 max-w-lg text-base leading-7 text-neutral-600 dark:text-neutral-300">
            pyDreamplet is designed for developers, analysts, designers, and creative coders who want direct control over SVG geometry while staying in Python.
          </p>
        </div>

        <div class="grid gap-4 md:grid-cols-3">
          <article
            v-for="item in useCases"
            :key="item.title"
            class="rounded-lg border border-neutral-200 bg-neutral-50 p-5 dark:border-neutral-800 dark:bg-neutral-900"
          >
            <h3 class="text-base font-semibold text-neutral-950 dark:text-white">
              {{ item.title }}
            </h3>
            <p class="mt-3 text-sm leading-6 text-neutral-600 dark:text-neutral-300">
              {{ item.description }}
            </p>
            <NuxtLink
              :to="item.link"
              class="mt-4 inline-flex text-sm font-semibold text-teal-700 hover:text-teal-800 dark:text-teal-300 dark:hover:text-teal-200"
            >
              {{ item.linkLabel }}
            </NuxtLink>
          </article>
        </div>
      </div>
    </section>

    <section class="bg-neutral-50 px-6 py-14 dark:bg-neutral-950">
      <div class="mx-auto grid max-w-7xl gap-10 lg:grid-cols-2">
        <div>
          <h2 class="text-2xl font-semibold leading-9 text-neutral-950 dark:text-white">
            What pyDreamplet gives you for custom Python graphics
          </h2>
          <p class="mt-5 max-w-xl text-base leading-7 text-neutral-600 dark:text-neutral-300">
            Use high-level helpers when they fit, then drop down to SVG primitives whenever you need exact geometry, styling, or export behavior.
          </p>
        </div>

        <ul class="grid gap-3 text-sm leading-6 text-neutral-700 dark:text-neutral-300">
          <li
            v-for="capability in capabilities"
            :key="capability"
            class="flex gap-3"
          >
            <UIcon name="i-lucide-check" class="mt-1 size-4 shrink-0 text-teal-700 dark:text-teal-300" />
            <span>{{ capability }}</span>
          </li>
        </ul>
      </div>
    </section>

    <section class="bg-white px-6 py-14 dark:bg-neutral-950">
      <div class="mx-auto max-w-4xl">
        <h2 class="text-2xl font-semibold leading-9 text-neutral-950 dark:text-white">
          pyDreamplet questions
        </h2>
        <div class="mt-7 divide-y divide-neutral-200 border-y border-neutral-200 dark:divide-neutral-800 dark:border-neutral-800">
          <article
            v-for="item in faqs"
            :key="item.question"
            class="py-5"
          >
            <h3 class="text-base font-semibold text-neutral-950 dark:text-white">
              {{ item.question }}
            </h3>
            <p class="mt-2 text-sm leading-6 text-neutral-600 dark:text-neutral-300">
              {{ item.answer }}
            </p>
          </article>
        </div>
      </div>
    </section>
  </main>
</template>
