<script setup lang="ts">
import { ref } from 'vue'

export interface VideoInfo {
  title: string
  thumbnail: string
  duration: string
  platform: string
  platformColor: string
  author: string
  formats: { label: string; size: string; quality: string }[]
}

defineProps<{
  video: VideoInfo
  sourceUrl: string
}>()

const emit = defineEmits<{
  back: []
}>()

const selectedFormat = ref(0)
const downloading = ref(false)

function handleDownload() {
  downloading.value = true
  setTimeout(() => {
    downloading.value = false
  }, 2000)
}
</script>

<template>
  <section class="relative flex flex-col items-center px-4 pt-28 pb-20">
    <div
      class="pointer-events-none absolute top-0 left-1/2 -translate-x-1/2 h-[400px] w-[500px] rounded-full bg-accent-glow blur-[160px] opacity-30"
    />

    <button
      @click="emit('back')"
      class="relative cursor-pointer mb-8 flex items-center gap-2 text-sm text-text-muted transition-colors duration-200 hover:text-accent"
    >
      <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" />
      </svg>
      返回提取新视频
    </button>

    <div class="relative w-full max-w-3xl rounded-2xl border border-border bg-bg-secondary/50 backdrop-blur-md overflow-hidden">
      <!-- Thumbnail -->
      <div class="relative aspect-video w-full bg-bg-tertiary overflow-hidden">
        <img
          :src="video.thumbnail"
          :alt="video.title"
          class="h-full w-full object-cover"
        />
        <div class="absolute bottom-3 right-3 rounded-lg bg-bg-primary/80 px-2.5 py-1 font-mono text-xs text-text-primary backdrop-blur-sm">
          {{ video.duration }}
        </div>
        <div
          class="absolute top-3 left-3 rounded-lg px-2.5 py-1 text-xs font-semibold backdrop-blur-sm"
          :style="{ backgroundColor: video.platformColor + '20', color: video.platformColor }"
        >
          {{ video.platform }}
        </div>
      </div>

      <!-- Info -->
      <div class="p-6">
        <h2 class="font-display text-xl font-bold leading-snug text-text-primary md:text-2xl">
          {{ video.title }}
        </h2>
        <p class="mt-2 text-sm text-text-muted">{{ video.author }}</p>

        <!-- Source URL -->
        <div class="mt-4 flex items-center gap-2 rounded-lg bg-bg-tertiary/60 px-3 py-2">
          <svg class="h-3.5 w-3.5 shrink-0 text-text-muted" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
          </svg>
          <span class="truncate font-mono text-xs text-text-muted">{{ sourceUrl }}</span>
        </div>

        <!-- Format selection -->
        <div class="mt-6">
          <h3 class="mb-3 text-sm font-semibold text-text-secondary">选择清晰度</h3>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="(fmt, i) in video.formats"
              :key="i"
              @click="selectedFormat = i"
              class="cursor-pointer rounded-xl border px-4 py-2.5 text-sm transition-all duration-200"
              :class="selectedFormat === i
                ? 'border-accent bg-accent-soft text-accent font-semibold'
                : 'border-border bg-bg-tertiary/40 text-text-secondary hover:border-border-hover hover:text-text-primary'"
            >
              <span class="block font-medium">{{ fmt.quality }}</span>
              <span class="block mt-0.5 text-xs opacity-60">{{ fmt.size }}</span>
            </button>
          </div>
        </div>

        <!-- Download button -->
        <button
          @click="handleDownload"
          :disabled="downloading"
          class="cursor-pointer mt-6 flex w-full items-center justify-center gap-2.5 rounded-xl bg-accent py-3.5 text-base font-bold text-bg-primary transition-all duration-200 hover:bg-accent-hover disabled:opacity-60"
        >
          <template v-if="!downloading">
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            下载视频
          </template>
          <template v-else>
            <svg class="h-5 w-5 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            下载中...
          </template>
        </button>
      </div>
    </div>
  </section>
</template>
