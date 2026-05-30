<script setup lang="ts">
const props = defineProps<{
  src: string
  alt?: string
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
</style>
