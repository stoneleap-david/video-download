<script setup lang="ts">
</script>

<template>
  <nav class="fixed top-4 left-4 right-4 z-50 mx-auto max-w-7xl">
    <div
      class="flex items-center justify-between rounded-2xl border border-border bg-bg-secondary/80 px-6 py-3 backdrop-blur-xl"
    >
      <div class="flex items-center gap-3">
        <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-accent-soft">
          <svg class="h-5 w-5 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
        </div>
        <span class="font-display text-xl font-bold tracking-wide text-text-primary">
          万能视频提取器
        </span>
      </div>

      <div class="hidden items-center gap-6 md:flex">
        <a href="#" class="cursor-pointer text-sm text-text-secondary transition-colors duration-200 hover:text-accent">
          首页
        </a>
        <a href="#" class="cursor-pointer text-sm text-text-secondary transition-colors duration-200 hover:text-accent">
          使用教程
        </a>
        <a href="#" class="cursor-pointer text-sm text-text-secondary transition-colors duration-200 hover:text-accent">
          支持平台
        </a>
      </div>

      <button class="cursor-pointer rounded-xl bg-accent px-5 py-2 text-sm font-semibold text-bg-primary transition-colors duration-200 hover:bg-accent-hover">
        开始使用
      </button>
    </div>
  </nav>
</template>
