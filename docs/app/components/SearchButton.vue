<script setup lang="ts">
withDefaults(defineProps<{
  label?: string
  fullLabel?: boolean
}>(), {
  label: 'Search',
  fullLabel: false
})

const open = ref(false)
const loaded = ref(false)

const openSearch = () => {
  loaded.value = true
  open.value = true
}

onMounted(() => {
  window.addEventListener('keydown', handleShortcut)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleShortcut)
})

function handleShortcut(event: KeyboardEvent) {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    openSearch()
  }
}
</script>

<template>
  <UButton
    icon="i-lucide-search"
    color="neutral"
    variant="outline"
    aria-label="Search documentation"
    @click="openSearch"
  >
    <span :class="fullLabel ? 'inline' : 'hidden sm:inline'">{{ label }}</span>
  </UButton>

  <LazySearchDialog
    v-if="loaded"
    v-model:open="open"
  />
</template>
