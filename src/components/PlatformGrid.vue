<script setup lang="ts">
const platforms = [
  { name: 'Bilibili', alias: 'B站', color: '#00A1D6' },
  { name: 'YouTube', alias: 'YouTube', color: '#FF0000' },
  { name: '抖音', alias: '抖音', color: '#FE2C55' },
  { name: '快手', alias: '快手', color: '#FF4906' },
  { name: '小红书', alias: '小红书', color: '#FF2442' },
  { name: '微博', alias: '微博', color: '#E6162D' },
]
</script>

<template>
  <div>
    <h2 class="mb-6 text-center font-display text-lg font-semibold tracking-wide text-text-muted">
      支持平台
    </h2>
    <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-6">
      <div
        v-for="platform in platforms"
        :key="platform.name"
        class="group cursor-pointer flex flex-col items-center gap-2 rounded-xl border border-border bg-bg-secondary/40 p-4 transition-all duration-200 hover:border-border-hover hover:bg-bg-secondary/80"
      >
        <div
          class="flex h-10 w-10 items-center justify-center rounded-lg transition-transform duration-200 group-hover:scale-110"
          :style="{ backgroundColor: platform.color + '18' }"
        >
          <span class="text-lg font-bold" :style="{ color: platform.color }">
            {{ platform.alias.charAt(0) }}
          </span>
        </div>
        <span class="text-xs font-medium text-text-secondary group-hover:text-text-primary transition-colors duration-200">
          {{ platform.alias }}
        </span>
      </div>
    </div>
  </div>
</template>
