<script setup lang="ts">
import UrlInput from '../components/UrlInput.vue'
import PlatformGrid from '../components/PlatformGrid.vue'
</script>

<template>
  <section class="relative flex flex-col items-center px-4 pt-32 pb-20">
    <div
      class="pointer-events-none absolute top-0 left-1/2 -translate-x-1/2 h-[480px] w-[640px] rounded-full bg-accent-glow blur-[160px] opacity-40"
    />

    <h1
      class="relative font-display text-5xl font-bold leading-tight tracking-tight text-text-primary md:text-6xl lg:text-7xl text-center"
    >
      全网视频<span class="text-accent">一键提取</span>
    </h1>

    <p class="relative mt-5 max-w-xl text-center text-lg leading-relaxed text-text-secondary">
      支持 B站、YouTube、抖音等主流平台，粘贴链接即可高速下载，无需登录
    </p>

    <div class="relative mt-10 w-full max-w-2xl">
      <UrlInput />
    </div>

    <div class="relative mt-20 w-full max-w-5xl">
      <PlatformGrid />
    </div>
  </section>
</template>
