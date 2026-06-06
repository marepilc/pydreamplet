<script setup lang="ts">
type DocSearchResult = {
  id: string
  title: string
  titles: string[]
  content: string
  snippets?: {
    title?: string
    content?: string
  }
}

const open = defineModel<boolean>('open', { default: false })
const query = ref('')
const results = ref<DocSearchResult[]>([])
const pending = ref(false)
const inputRoot = ref<HTMLElement | null>(null)
let searchRun = 0

const { search, status } = useSearchCollection('docs', {
  minHeading: 'h1',
  maxHeading: 'h3'
})

const trimmedQuery = computed(() => query.value.trim())

const visibleResults = computed(() => {
  if (trimmedQuery.value.length < 2) {
    return []
  }

  return results.value
})

const runSearch = async () => {
  const run = ++searchRun

  if (trimmedQuery.value.length < 2) {
    results.value = []
    return
  }

  pending.value = true
  try {
    const nextResults = await search(trimmedQuery.value, {
      limit: 12,
      fields: ['title', 'content'],
      snippet: {
        columns: ['content'],
        around: 16,
        tag: 'mark'
      }
    })

    if (run === searchRun) {
      results.value = nextResults
    }
  } finally {
    if (run === searchRun) {
      pending.value = false
    }
  }
}

const focusInput = async () => {
  await nextTick()
  requestAnimationFrame(() => {
    inputRoot.value?.querySelector('input')?.focus()
  })
}

const closeSearch = () => {
  open.value = false
}

const resultContext = (result: DocSearchResult) => {
  return [...result.titles, result.title].filter(Boolean).join(' / ')
}

watch(trimmedQuery, async () => {
  await runSearch()
})

watch(open, (value) => {
  if (value) {
    focusInput()
  }
}, { flush: 'post' })

onMounted(() => {
  if (open.value) {
    focusInput()
  }
})
</script>

<template>
  <UModal
    v-model:open="open"
    title="Search"
    :ui="{ content: 'sm:max-w-2xl' }"
  >
    <template #body>
      <div class="space-y-4">
        <div ref="inputRoot">
          <UInput
            v-model="query"
            icon="i-lucide-search"
            placeholder="Search documentation"
            size="lg"
            color="primary"
            autocomplete="off"
            enterkeyhint="search"
            :loading="pending || status === 'loading'"
            class="w-full"
            :ui="{
              base: 'focus-visible:!ring-teal-500 dark:focus-visible:!ring-teal-400'
            }"
          />
        </div>

        <div
          v-if="trimmedQuery.length < 2"
          class="rounded-lg border border-neutral-200 px-4 py-8 text-center text-sm text-neutral-500 dark:border-neutral-800 dark:text-neutral-400"
        >
          Enter at least two characters.
        </div>

        <div
          v-else-if="!pending && visibleResults.length === 0"
          class="rounded-lg border border-neutral-200 px-4 py-8 text-center text-sm text-neutral-500 dark:border-neutral-800 dark:text-neutral-400"
        >
          No matching pages.
        </div>

        <nav
          v-else
          class="max-h-[55vh] overflow-y-auto"
          aria-label="Search results"
        >
          <ul class="space-y-1">
            <li
              v-for="result in visibleResults"
              :key="result.id"
            >
              <NuxtLink
                :to="result.id"
                class="block rounded-lg border border-transparent px-3 py-3 hover:border-neutral-200 hover:bg-neutral-50 dark:hover:border-neutral-800 dark:hover:bg-neutral-900"
                @click="closeSearch"
              >
                <span class="block text-sm font-semibold text-neutral-950 dark:text-white">
                  {{ result.title }}
                </span>
                <span
                  v-if="resultContext(result)"
                  class="mt-1 block text-xs text-neutral-500 dark:text-neutral-400"
                >
                  {{ resultContext(result) }}
                </span>
                <span
                  v-if="result.snippets?.content"
                  class="search-snippet mt-2 block text-sm leading-6 text-neutral-600 dark:text-neutral-300"
                  v-html="result.snippets.content"
                />
                <span
                  v-else-if="result.content"
                  class="mt-2 block line-clamp-2 text-sm leading-6 text-neutral-600 dark:text-neutral-300"
                >
                  {{ result.content }}
                </span>
              </NuxtLink>
            </li>
          </ul>
        </nav>
      </div>
    </template>
  </UModal>
</template>

<style scoped>
.search-snippet :deep(mark) {
  border-radius: 0.2rem;
  background: color-mix(in oklab, var(--ui-primary) 22%, transparent);
  color: inherit;
  padding: 0.05rem 0.16rem;
}
</style>
