<script setup lang="ts">
const props = defineProps<{
  src: string
  darkSrc?: string
  alt?: string
  size?: 'fit' | 'original'
}>()

const { data: svgMarkup } = await useAsyncData(`svg-preview:${props.src}`, () => {
  return $fetch<string>(props.src, {
    responseType: 'text'
  })
})

const { data: darkSvgMarkup } = await useAsyncData(
  `svg-preview:${props.darkSrc ?? props.src}:dark`,
  () => {
    if (!props.darkSrc) {
      return null
    }

    return $fetch<string>(props.darkSrc, {
      responseType: 'text'
    })
  }
)

const colorMode = useColorMode()
const activeSvgMarkup = computed(() => {
  if (colorMode.value === 'dark' && darkSvgMarkup.value) {
    return darkSvgMarkup.value
  }

  return svgMarkup.value
})
</script>

<template>
  <figure
    class="mt-6 overflow-hidden rounded-lg border border-neutral-200 bg-white text-neutral-900 dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-100"
  >
    <div
      v-if="activeSvgMarkup"
      class="svg-preview p-4"
      :class="{ 'svg-preview--original': size === 'original' }"
      role="img"
      :aria-label="alt"
      v-html="activeSvgMarkup"
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
