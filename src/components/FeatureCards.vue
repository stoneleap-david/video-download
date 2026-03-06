<script setup lang="ts">
const features = [
  {
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>`,
    title: '免登录下载',
    desc: '无需 Cookie，无需扫码，粘贴即下',
  },
  {
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    title: '极速解析',
    desc: '秒级响应，支持多清晰度选择',
  },
  {
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
    title: '全平台覆盖',
    desc: 'B站、YouTube、抖音、快手等主流平台',
  },
]
</script>

<template>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
    <div
      v-for="(feature, i) in features"
      :key="i"
      class="group rounded-2xl border border-border bg-bg-secondary/30 p-5 transition-all duration-300 hover:border-accent/30 hover:bg-accent-soft/30"
    >
      <div class="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-accent-soft text-accent">
        <span class="h-5 w-5 [&>svg]:h-5 [&>svg]:w-5" v-html="feature.icon" />
      </div>
      <h3 class="font-display text-base font-semibold text-text-primary">{{ feature.title }}</h3>
      <p class="mt-1 text-sm leading-relaxed text-text-muted">{{ feature.desc }}</p>
    </div>
  </div>
</template>
