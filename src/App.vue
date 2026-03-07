<script setup lang="ts">
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import Home from './views/Home.vue'
import VideoResult from './components/VideoResult.vue'
import type { VideoInfo } from './components/VideoResult.vue'

const API_BASE = 'http://127.0.0.1:8000'

const currentView = ref<'home' | 'result'>('home')
const sourceUrl = ref('')
const videoInfo = ref<VideoInfo | null>(null)
const parseError = ref('')
const parsing = ref(false)

async function handleExtract(url: string) {
  sourceUrl.value = url
  parseError.value = ''
  parsing.value = true

  try {
    const res = await fetch(`${API_BASE}/api/parse?url=${encodeURIComponent(url)}`)
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || '解析失败')
    }
    videoInfo.value = await res.json()
    currentView.value = 'result'
  } catch (e: any) {
    parseError.value = e.message || '网络错误，请重试'
  } finally {
    parsing.value = false
  }
}

function handleBack() {
  currentView.value = 'home'
  videoInfo.value = null
  parseError.value = ''
}

const downloading = ref(false)

async function handleDownload(formatId: string) {
  if (downloading.value) return
  downloading.value = true

  try {
    const res = await fetch(
      `${API_BASE}/api/download?url=${encodeURIComponent(sourceUrl.value)}&format_id=${encodeURIComponent(formatId)}`
    )
    if (!res.ok) throw new Error('下载失败')

    const blob = await res.blob()
    const disposition = res.headers.get('Content-Disposition') || ''
    const match = disposition.match(/filename\*=UTF-8''(.+)/)
    const filename = match ? decodeURIComponent(match[1]) : 'video.mp4'

    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = filename
    a.click()
    URL.revokeObjectURL(a.href)
  } catch (e: any) {
    alert(e.message || '下载出错，请重试')
  } finally {
    downloading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-bg-primary">
    <Navbar />
    <main class="flex-1">
      <Transition name="fade" mode="out-in">
        <Home
          v-if="currentView === 'home'"
          :loading="parsing"
          :error="parseError"
          @extract="handleExtract"
        />
        <VideoResult
          v-else-if="videoInfo"
          :video="videoInfo"
          :source-url="sourceUrl"
          :downloading="downloading"
          @back="handleBack"
          @download="handleDownload"
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
