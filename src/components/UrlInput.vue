<script setup lang="ts">
import { ref } from 'vue'

const url = ref('')
const isLoading = ref(false)

function handleSubmit() {
  if (!url.value.trim()) return
  isLoading.value = true
  // TODO: call backend API
  setTimeout(() => {
    isLoading.value = false
  }, 2000)
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="relative">
    <div
      class="flex items-center gap-3 rounded-2xl border border-border bg-bg-secondary/60 p-2 backdrop-blur-md transition-colors duration-200 focus-within:border-accent/50"
    >
      <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-bg-tertiary text-text-muted">
        <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
          <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
        </svg>
      </div>

      <input
        v-model="url"
        type="url"
        placeholder="粘贴视频链接，支持 B站 / YouTube / 抖音 / 快手..."
        class="flex-1 bg-transparent font-mono text-sm text-text-primary placeholder:text-text-muted outline-none"
      />

      <button
        type="submit"
        :disabled="isLoading || !url.trim()"
        class="cursor-pointer shrink-0 rounded-xl bg-accent px-6 py-2.5 text-sm font-semibold text-bg-primary transition-all duration-200 hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-40"
      >
        <span v-if="!isLoading">提取视频</span>
        <span v-else class="flex items-center gap-2">
          <svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
          </svg>
          解析中...
        </span>
      </button>
    </div>
  </form>
</template>
