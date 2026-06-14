<script setup lang="ts">
defineProps<{
  version: string
}>()
</script>

<template>
  <UBadge
    class="mb-3"
    color="neutral"
    variant="subtle"
    size="sm"
  >
    Since v{{ version }}
  </UBadge>
</template>
