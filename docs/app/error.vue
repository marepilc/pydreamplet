<script setup lang="ts">
const error = useError()

useSeoMeta({
  title: error.value?.statusCode === 404 ? 'Page not found' : 'Error',
  robots: 'noindex, nofollow'
})
</script>

<template>
  <main class="grid min-h-screen place-items-center bg-white px-6 text-neutral-950 dark:bg-neutral-950 dark:text-white">
    <div class="max-w-lg text-center">
      <p class="text-sm font-semibold text-teal-700 dark:text-teal-300">
        {{ error?.statusCode || 500 }}
      </p>
      <h1 class="mt-3 text-3xl font-semibold">
        {{ error?.statusCode === 404 ? 'Page not found' : 'Something went wrong' }}
      </h1>
      <p class="mt-4 text-neutral-600 dark:text-neutral-300">
        {{ error?.statusMessage || 'The requested page could not be displayed.' }}
      </p>
      <UButton
        to="/"
        icon="i-lucide-home"
        class="mt-7"
        @click="clearError({ redirect: '/' })"
      >
        Back to pyDreamplet
      </UButton>
    </div>
  </main>
</template>
