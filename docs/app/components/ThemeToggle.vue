<script setup lang="ts">
const colorMode = useColorMode()
const resolvedMode = ref<'light' | 'dark'>('light')

const syncResolvedMode = () => {
  if (import.meta.client) {
    resolvedMode.value = document.documentElement.classList.contains('dark') ? 'dark' : 'light'
  }
}

onMounted(syncResolvedMode)

watch(
  () => [colorMode.value, colorMode.preference],
  () => nextTick(syncResolvedMode)
)

const icon = computed(() => resolvedMode.value === 'dark' ? 'i-lucide-moon' : 'i-lucide-sun')
const label = computed(() => resolvedMode.value === 'dark' ? 'Switch to light mode' : 'Switch to dark mode')

const toggleTheme = () => {
  const nextMode = resolvedMode.value === 'dark' ? 'light' : 'dark'

  resolvedMode.value = nextMode
  colorMode.preference = nextMode
}
</script>

<template>
  <ClientOnly>
    <UButton
      color="neutral"
      variant="ghost"
      :aria-label="label"
      @click="toggleTheme"
    >
      <UIcon :key="icon" :name="icon" class="size-5" />
    </UButton>

    <template #fallback>
      <div class="size-8" />
    </template>
  </ClientOnly>
</template>
