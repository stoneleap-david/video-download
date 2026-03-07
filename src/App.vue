<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface VideoFormat {
  format_id: string
  quality: string
  size: string
}

interface VideoInfo {
  title: string
  duration: string
  platform: string
  platformColor: string
  author: string
  formats: VideoFormat[]
}

const API_BASE = 'http://127.0.0.1:8000'

const url = ref('')
const videoInfo = ref<VideoInfo | null>(null)
const sourceUrl = ref('')
const parseError = ref('')
const parsing = ref(false)
const downloading = ref(false)
const selectedFormat = ref(0)
const mounted = ref(false)

onMounted(() => {
  setTimeout(() => { mounted.value = true }, 100)
})

async function handleExtract() {
  const input = url.value.trim()
  if (!input || parsing.value) return

  sourceUrl.value = input
  parseError.value = ''
  parsing.value = true
  videoInfo.value = null
  selectedFormat.value = 0

  try {
    const res = await fetch(`${API_BASE}/api/parse?url=${encodeURIComponent(input)}`)
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || '解析失败')
    }
    videoInfo.value = await res.json()
  } catch (e: any) {
    parseError.value = e.message || '网络错误，请重试'
  } finally {
    parsing.value = false
  }
}

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
    const filename = match?.[1] ? decodeURIComponent(match[1]) : 'video.mp4'

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
  <div class="app-shell min-h-screen flex flex-col relative overflow-hidden">
    <!-- Animated grid background -->
    <div class="grid-bg" />
    <div class="scan-line" />

    <main class="flex-1 flex flex-col items-center px-4 pt-16 pb-16 relative z-10">
      <!-- Logo + Title -->
      <div
        class="flex flex-col items-center mb-10 transition-all duration-700"
        :class="mounted ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'"
      >
        <div class="hex-icon mb-4">
          <svg class="h-7 w-7 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
        </div>
        <h1 class="font-display text-2xl font-bold tracking-[0.2em] uppercase text-text-primary">
          Video <span class="text-accent">Extract</span>
        </h1>
        <div class="mt-2 flex items-center gap-3 text-[10px] font-mono tracking-[0.15em] uppercase text-text-muted">
          <span class="inline-block h-px w-6 bg-accent/30" />
          Universal Video Downloader
          <span class="inline-block h-px w-6 bg-accent/30" />
        </div>
      </div>

      <!-- URL Input -->
      <form
        @submit.prevent="handleExtract"
        class="w-full max-w-2xl transition-all duration-700 delay-200"
        :class="mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'"
      >
        <div class="input-container" :class="{ 'input-error': parseError, 'input-active': parsing }">
          <div class="input-border" />
          <div class="flex items-center gap-2 relative z-10 p-1.5">
            <div class="flex h-9 w-9 shrink-0 items-center justify-center text-accent/40">
              <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </div>

            <input
              v-model="url"
              type="url"
              placeholder="PASTE VIDEO URL — Bilibili / YouTube / Douyin / Kuaishou..."
              class="flex-1 bg-transparent font-mono text-xs tracking-wide text-text-primary placeholder:text-text-muted/40 placeholder:tracking-wider outline-none"
              :disabled="parsing"
            />

            <button
              type="submit"
              :disabled="parsing || !url.trim()"
              class="extract-btn shrink-0"
            >
              <span v-if="!parsing" class="flex items-center gap-2">
                <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="13 17 18 12 13 7" /><polyline points="6 17 11 12 6 7" />
                </svg>
                EXTRACT
              </span>
              <span v-else class="flex items-center gap-2">
                <svg class="h-3.5 w-3.5 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                SCANNING
              </span>
            </button>
          </div>
        </div>

        <p v-if="parseError" class="mt-3 text-center font-mono text-xs tracking-wide text-danger">
          [ ERROR ] {{ parseError }}
        </p>
      </form>

      <!-- Result Card -->
      <Transition name="slide">
        <div v-if="videoInfo" class="w-full max-w-2xl mt-8">
          <div class="result-card">
            <!-- Corner decorations -->
            <div class="corner-tl" /><div class="corner-tr" /><div class="corner-bl" /><div class="corner-br" />

            <!-- Status bar -->
            <div class="flex items-center gap-2 px-5 py-2.5 border-b border-border">
              <span class="relative flex h-1.5 w-1.5">
                <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent-2 opacity-60" />
                <span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-accent-2" />
              </span>
              <span class="font-mono text-[10px] tracking-[0.15em] uppercase text-accent-2">TARGET ACQUIRED</span>
              <span class="ml-auto font-mono text-[10px] text-text-muted">{{ videoInfo.duration }}</span>
            </div>

            <!-- Video info -->
            <div class="px-5 py-4">
              <div class="flex items-start gap-3">
                <div
                  class="flex h-9 w-9 shrink-0 items-center justify-center rounded text-xs font-bold font-display border"
                  :style="{
                    backgroundColor: videoInfo.platformColor + '10',
                    color: videoInfo.platformColor,
                    borderColor: videoInfo.platformColor + '30',
                  }"
                >
                  {{ videoInfo.platform.charAt(0) }}
                </div>
                <div class="flex-1 min-w-0">
                  <h2 class="text-sm font-semibold leading-snug text-text-primary">
                    {{ videoInfo.title }}
                  </h2>
                  <div class="mt-1.5 flex flex-wrap items-center gap-2 font-mono text-[10px] text-text-muted tracking-wide">
                    <span>{{ videoInfo.author }}</span>
                    <span class="text-accent/20">|</span>
                    <span
                      class="rounded-sm px-1.5 py-0.5 font-bold tracking-wider uppercase"
                      :style="{ backgroundColor: videoInfo.platformColor + '15', color: videoInfo.platformColor }"
                    >{{ videoInfo.platform }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Formats + Download -->
            <div class="border-t border-border px-5 py-4">
              <div class="flex flex-wrap items-center gap-2">
                <button
                  v-for="(fmt, i) in videoInfo.formats"
                  :key="fmt.format_id"
                  @click="selectedFormat = i"
                  class="format-btn"
                  :class="{ active: selectedFormat === i }"
                >
                  <span class="font-bold">{{ fmt.quality }}</span>
                  <span class="opacity-40 ml-1">{{ fmt.size }}</span>
                </button>

                <button
                  @click="handleDownload(videoInfo?.formats?.[selectedFormat]?.format_id ?? '')"
                  :disabled="downloading"
                  class="download-btn ml-auto"
                >
                  <template v-if="!downloading">
                    <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="7 10 12 15 17 10" />
                      <line x1="12" y1="15" x2="12" y2="3" />
                    </svg>
                    DOWNLOAD
                  </template>
                  <template v-else>
                    <svg class="h-3.5 w-3.5 animate-spin" viewBox="0 0 24 24" fill="none">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" />
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    DOWNLOADING...
                  </template>
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Empty state -->
      <div
        v-if="!videoInfo && !parsing"
        class="mt-14 flex flex-col items-center gap-4 transition-all duration-700 delay-400"
        :class="mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'"
      >
        <div class="flex items-center gap-4 font-mono text-[10px] tracking-[0.2em] uppercase text-text-muted/30">
          <span class="h-px w-10 bg-gradient-to-r from-transparent to-accent/20" />
          SUPPORTED PLATFORMS
          <span class="h-px w-10 bg-gradient-to-l from-transparent to-accent/20" />
        </div>
        <div class="flex flex-wrap justify-center gap-3">
          <span v-for="p in ['Bilibili', 'YouTube', '抖音', '快手', '小红书', '微博']" :key="p"
            class="platform-tag">{{ p }}</span>
        </div>
      </div>
    </main>

    <footer class="relative z-10 border-t border-border-dim px-4 py-5">
      <p class="text-center font-mono text-[10px] tracking-[0.15em] text-text-muted/25 uppercase">
        Personal Use Only · Powered by David
      </p>
    </footer>
  </div>
</template>

<style>
/* ===== Background ===== */
.grid-bg {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: grid-drift 8s linear infinite;
  z-index: 0;
}

.grid-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(0, 240, 255, 0.06) 0%, transparent 60%),
              radial-gradient(ellipse at 50% 100%, rgba(16, 185, 129, 0.04) 0%, transparent 60%);
}

.scan-line {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, rgba(0, 240, 255, 0.15) 50%, transparent 100%);
  animation: scanline 6s linear infinite;
  z-index: 1;
  pointer-events: none;
}

/* ===== Hex Icon ===== */
.hex-icon {
  position: relative;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 240, 255, 0.05);
  border: 1px solid rgba(0, 240, 255, 0.15);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}

/* ===== Input Container ===== */
.input-container {
  position: relative;
  background: rgba(12, 16, 23, 0.8);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  overflow: hidden;
}

.input-border {
  position: absolute;
  inset: 0;
  border-radius: 12px;
  border: 1px solid rgba(0, 240, 255, 0.12);
  pointer-events: none;
  transition: all 0.3s ease;
}

.input-container:focus-within .input-border {
  border-color: rgba(0, 240, 255, 0.35);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.06), inset 0 0 20px rgba(0, 240, 255, 0.02);
}

.input-container.input-error .input-border {
  border-color: rgba(244, 63, 94, 0.4);
}

.input-container.input-active .input-border {
  border-color: rgba(0, 240, 255, 0.5);
  box-shadow: 0 0 30px rgba(0, 240, 255, 0.08);
}

/* ===== Extract Button ===== */
.extract-btn {
  position: relative;
  padding: 8px 20px;
  background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(0, 240, 255, 0.05));
  border: 1px solid rgba(0, 240, 255, 0.3);
  border-radius: 8px;
  color: #00F0FF;
  font-family: 'Orbitron', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.15em;
  cursor: pointer;
  transition: all 0.25s ease;
}

.extract-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(0, 240, 255, 0.25), rgba(0, 240, 255, 0.1));
  border-color: rgba(0, 240, 255, 0.5);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.15);
}

.extract-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

/* ===== Result Card ===== */
.result-card {
  position: relative;
  background: rgba(12, 16, 23, 0.85);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(0, 240, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  animation: flicker 4s ease-in-out infinite;
}

.result-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0, 240, 255, 0.03) 0%, transparent 40%);
  pointer-events: none;
}

.corner-tl, .corner-tr, .corner-bl, .corner-br {
  position: absolute;
  width: 12px;
  height: 12px;
  z-index: 2;
}
.corner-tl { top: -1px; left: -1px; border-top: 2px solid rgba(0, 240, 255, 0.5); border-left: 2px solid rgba(0, 240, 255, 0.5); }
.corner-tr { top: -1px; right: -1px; border-top: 2px solid rgba(0, 240, 255, 0.5); border-right: 2px solid rgba(0, 240, 255, 0.5); }
.corner-bl { bottom: -1px; left: -1px; border-bottom: 2px solid rgba(0, 240, 255, 0.5); border-left: 2px solid rgba(0, 240, 255, 0.5); }
.corner-br { bottom: -1px; right: -1px; border-bottom: 2px solid rgba(0, 240, 255, 0.5); border-right: 2px solid rgba(0, 240, 255, 0.5); }

/* ===== Format Buttons ===== */
.format-btn {
  padding: 6px 12px;
  border: 1px solid rgba(0, 240, 255, 0.1);
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-secondary);
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: 0.03em;
}

.format-btn:hover {
  border-color: rgba(0, 240, 255, 0.25);
  color: var(--color-text-primary);
}

.format-btn.active {
  border-color: rgba(0, 240, 255, 0.5);
  background: rgba(0, 240, 255, 0.08);
  color: #00F0FF;
  box-shadow: 0 0 12px rgba(0, 240, 255, 0.08);
}

/* ===== Download Button ===== */
.download-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: linear-gradient(135deg, #00F0FF, #00C4D0);
  border: none;
  border-radius: 8px;
  color: #06080D;
  font-family: 'Orbitron', sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  cursor: pointer;
  transition: all 0.25s ease;
}

.download-btn:hover:not(:disabled) {
  box-shadow: 0 0 24px rgba(0, 240, 255, 0.3);
  transform: translateY(-1px);
}

.download-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* ===== Platform Tags ===== */
.platform-tag {
  padding: 4px 12px;
  border: 1px solid rgba(0, 240, 255, 0.06);
  border-radius: 4px;
  font-family: 'Exo 2', sans-serif;
  font-size: 11px;
  color: var(--color-text-muted);
  transition: all 0.3s ease;
}

.platform-tag:hover {
  border-color: rgba(0, 240, 255, 0.2);
  color: rgba(0, 240, 255, 0.6);
}

/* ===== Transitions ===== */
.slide-enter-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-leave-active {
  transition: all 0.2s ease-in;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(16px) scale(0.98);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
