<script setup lang="ts">
import UrlInput from '../components/UrlInput.vue'
import PlatformGrid from '../components/PlatformGrid.vue'
import FeatureCards from '../components/FeatureCards.vue'

const emit = defineEmits<{
  extract: [url: string]
}>()
</script>

<template>
  <section class="relative flex flex-col items-center px-4 pt-28 pb-20">
    <div
      class="pointer-events-none absolute top-0 left-1/2 -translate-x-1/2 h-[480px] w-[640px] rounded-full bg-accent-glow blur-[160px] opacity-40"
    />

    <div class="relative inline-flex items-center gap-2 rounded-full border border-accent/20 bg-accent-soft/40 px-4 py-1.5 text-xs font-medium text-accent">
      <span class="relative flex h-2 w-2">
        <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-60"></span>
        <span class="relative inline-flex h-2 w-2 rounded-full bg-accent"></span>
      </span>
      免费使用 · 无需登录 · 极速解析
    </div>

    <h1
      class="relative mt-6 font-display text-5xl font-bold leading-tight tracking-tight text-text-primary md:text-6xl lg:text-7xl text-center"
    >
      全网视频<span class="text-accent">一键提取</span>
    </h1>

    <p class="relative mt-5 max-w-lg text-center text-lg leading-relaxed text-text-secondary">
      粘贴链接，秒级解析，支持多清晰度高速下载
    </p>

    <div class="relative mt-10 w-full max-w-2xl">
      <UrlInput @extract="(url) => emit('extract', url)" />
    </div>

    <div class="relative mt-16 w-full max-w-3xl">
      <FeatureCards />
    </div>

    <div class="relative mt-16 w-full max-w-5xl">
      <PlatformGrid />
    </div>
  </section>
</template>
