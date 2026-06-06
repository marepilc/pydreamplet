<script setup lang="ts">
const props = defineProps<{
  src: string
  alt?: string
  size?: 'fit' | 'original'
}>()

const { data: svgMarkup } = await useAsyncData(`svg-preview:${props.src}`, () => {
  return $fetch<string>(props.src, {
    responseType: 'text'
  })
})
</script>

<template>
  <figure
    class="mt-6 overflow-hidden rounded-lg border border-neutral-200 bg-white text-neutral-900 dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-100"
  >
    <div
      v-if="svgMarkup"
      class="svg-preview p-4"
      :class="{ 'svg-preview--original': size === 'original' }"
      role="img"
      :aria-label="alt"
      v-html="svgMarkup"
    />
  </figure>
</template>

<style scoped>
.svg-preview :deep(svg) {
  display: block;
  width: 100%;
  height: auto;
}

.svg-preview--original {
  display: flex;
  justify-content: center;
}

.svg-preview--original :deep(svg) {
  width: auto;
  max-width: 100%;
}
</style>
