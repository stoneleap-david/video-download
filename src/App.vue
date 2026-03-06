<script setup lang="ts">
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import Home from './views/Home.vue'
import VideoResult from './components/VideoResult.vue'
import type { VideoInfo } from './components/VideoResult.vue'

const currentView = ref<'home' | 'result'>('home')
const sourceUrl = ref('')

const mockVideo = ref<VideoInfo>({
  title: '',
  thumbnail: '',
  duration: '',
  platform: '',
  platformColor: '',
  author: '',
  formats: [],
})

const mockDataMap: Record<string, VideoInfo> = {
  bilibili: {
    title: '【4K】这可能是B站画质最好的风景视频',
    thumbnail: 'https://picsum.photos/seed/bili/800/450',
    duration: '12:34',
    platform: 'Bilibili',
    platformColor: '#00A1D6',
    author: '@自然纪录片',
    formats: [
      { label: '4K', quality: '4K 超清', size: '680 MB' },
      { label: '1080P', quality: '1080P 高清', size: '320 MB' },
      { label: '720P', quality: '720P', size: '180 MB' },
    ],
  },
  youtube: {
    title: 'The Most Beautiful Scenery on Earth - 4K Ultra HD',
    thumbnail: 'https://picsum.photos/seed/yt/800/450',
    duration: '25:10',
    platform: 'YouTube',
    platformColor: '#FF0000',
    author: '@NatureChannel',
    formats: [
      { label: '4K', quality: '4K 60fps', size: '1.2 GB' },
      { label: '1080P', quality: '1080P 60fps', size: '480 MB' },
      { label: '720P', quality: '720P', size: '220 MB' },
      { label: '360P', quality: '360P', size: '85 MB' },
    ],
  },
  default: {
    title: '短视频精选合集 - 今日热门推荐',
    thumbnail: 'https://picsum.photos/seed/video/800/450',
    duration: '03:22',
    platform: '抖音',
    platformColor: '#FE2C55',
    author: '@热门视频',
    formats: [
      { label: '1080P', quality: '1080P 高清', size: '45 MB' },
      { label: '720P', quality: '720P', size: '22 MB' },
    ],
  },
}

function handleExtract(url: string) {
  sourceUrl.value = url
  const lower = url.toLowerCase()
  if (lower.includes('bilibili') || lower.includes('b23')) {
    mockVideo.value = mockDataMap.bilibili
  } else if (lower.includes('youtube') || lower.includes('youtu.be')) {
    mockVideo.value = mockDataMap.youtube
  } else {
    mockVideo.value = mockDataMap.default
  }
  currentView.value = 'result'
}

function handleBack() {
  currentView.value = 'home'
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-bg-primary">
    <Navbar />
    <main class="flex-1">
      <Transition name="fade" mode="out-in">
        <Home v-if="currentView === 'home'" @extract="handleExtract" />
        <VideoResult
          v-else
          :video="mockVideo"
          :source-url="sourceUrl"
          @back="handleBack"
        />
      </Transition>
    </main>
    <Footer />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
