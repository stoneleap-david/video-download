<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  extract: [url: string]
}>()

const url = ref('')
const isLoading = ref(false)

function handleSubmit() {
  if (!url.value.trim()) return
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
    emit('extract', url.value.trim())
    url.value = ''
  }, 1500)
}

async function handlePaste() {
  try {
    const text = await navigator.clipboard.readText()
    if (text) {
      url.value = text
      handleSubmit()
    }
  } catch {
    // clipboard permission denied, ignore
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="relative">
    <div
      class="flex items-center gap-3 rounded-2xl border border-border bg-bg-secondary/60 p-2 backdrop-blur-md transition-all duration-200 focus-within:border-accent/50 focus-within:shadow-[0_0_24px_rgba(16,185,129,0.08)]"
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
        type="button"
        @click="handlePaste"
        class="cursor-pointer hidden shrink-0 items-center gap-1.5 rounded-lg border border-border px-3 py-2 text-xs text-text-muted transition-colors duration-200 hover:border-border-hover hover:text-text-secondary sm:flex"
      >
        <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
        </svg>
        粘贴
      </button>

      <button
        type="submit"
        :disabled="isLoading || !url.trim()"
        class="cursor-pointer shrink-0 rounded-xl bg-accent px-6 py-2.5 text-sm font-semibold text-bg-primary transition-all duration-200 hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-40"
      >
        <span v-if="!isLoading">提取视频</span>
        <span v-else class="flex items-center gap-2">
          <svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          解析中...
        </span>
      </button>
    </div>
  </form>
</template>
