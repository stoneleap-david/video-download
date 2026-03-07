<script setup lang="ts">
import { ref } from 'vue'

export interface VideoInfo {
  title: string
  thumbnail: string
  duration: string
  platform: string
  platformColor: string
  author: string
  formats: { format_id: string; size: string; quality: string }[]
}

interface TranscriptSegment {
  time: string
  text: string
}

const props = defineProps<{
  video: VideoInfo
  sourceUrl: string
  downloading?: boolean
}>()

const emit = defineEmits<{
  back: []
  download: [formatId: string]
}>()

const API_BASE = 'http://127.0.0.1:8000'

const selectedFormat = ref(0)
const transcribing = ref(false)
const transcriptText = ref('')
const transcriptSegments = ref<TranscriptSegment[]>([])
const transcriptLang = ref('')
const showTranscript = ref(false)
const transcriptError = ref('')

async function extractText() {
  transcribing.value = true
  transcriptError.value = ''
  transcriptText.value = ''
  transcriptSegments.value = []
  showTranscript.value = true

  try {
    const res = await fetch(`${API_BASE}/api/transcribe?url=${encodeURIComponent(props.sourceUrl)}`)
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: '识别失败' }))
      throw new Error(err.detail || '识别失败')
    }
    const data = await res.json()
    transcriptText.value = data.full_text || ''
    transcriptSegments.value = data.segments || []
    transcriptLang.value = data.language || ''
  } catch (e: any) {
    transcriptError.value = e.message || '语音识别失败'
  }
  transcribing.value = false
}

function copyText() {
  navigator.clipboard.writeText(transcriptText.value)
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
      <!-- Video info header -->
      <div class="p-6 pb-0">
        <div class="flex items-start gap-4">
          <div
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-lg font-bold"
            :style="{ backgroundColor: video.platformColor + '18', color: video.platformColor }"
          >
            {{ video.platform.charAt(0) }}
          </div>
          <div class="flex-1 min-w-0">
            <h2 class="font-display text-xl font-bold leading-snug text-text-primary md:text-2xl">
              {{ video.title }}
            </h2>
            <div class="mt-2 flex flex-wrap items-center gap-3 text-sm text-text-muted">
              <span>{{ video.author }}</span>
              <span class="text-border">|</span>
              <span
                class="rounded-md px-2 py-0.5 text-xs font-medium"
                :style="{ backgroundColor: video.platformColor + '18', color: video.platformColor }"
              >{{ video.platform }}</span>
              <span class="text-border">|</span>
              <span class="font-mono">{{ video.duration }}</span>
            </div>
          </div>
        </div>

        <div class="mt-4 flex items-center gap-2 rounded-lg bg-bg-tertiary/60 px-3 py-2">
          <svg class="h-3.5 w-3.5 shrink-0 text-text-muted" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
          </svg>
          <span class="truncate font-mono text-xs text-text-muted">{{ sourceUrl }}</span>
        </div>
      </div>

      <div class="p-6">
        <!-- Format selection -->
        <div>
          <h3 class="mb-3 text-sm font-semibold text-text-secondary">选择清晰度</h3>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="(fmt, i) in video.formats"
              :key="fmt.format_id"
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

        <!-- Extract Text section -->
        <div class="mt-6">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-semibold text-text-secondary">提取文字</h3>
            <button
              v-if="!showTranscript"
              @click="extractText"
              :disabled="transcribing"
              class="cursor-pointer flex items-center gap-1.5 rounded-lg border border-border bg-bg-tertiary/40 px-3 py-1.5 text-xs text-text-secondary transition-all duration-200 hover:border-accent hover:text-accent disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" y1="19" x2="12" y2="23" />
                <line x1="8" y1="23" x2="16" y2="23" />
              </svg>
              语音识别
            </button>
          </div>

          <p v-if="!showTranscript" class="text-xs text-text-muted">
            使用 AI 语音识别提取视频中的文字内容（首次加载模型可能较慢）
          </p>

          <Transition name="slide">
            <div v-if="showTranscript" class="rounded-xl border border-border bg-bg-primary/80 p-4">
              <div class="mb-2 flex items-center justify-between">
                <span class="text-xs font-medium text-text-secondary">
                  识别结果
                  <span v-if="transcriptLang" class="ml-1 opacity-60">({{ transcriptLang }})</span>
                </span>
                <div class="flex items-center gap-2">
                  <button
                    v-if="transcriptText"
                    @click="copyText"
                    class="cursor-pointer text-xs text-text-muted transition-colors hover:text-accent"
                  >
                    复制全文
                  </button>
                  <button
                    @click="showTranscript = false"
                    class="cursor-pointer text-text-muted transition-colors hover:text-text-primary"
                  >
                    <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                    </svg>
                  </button>
                </div>
              </div>

              <div
                v-if="transcribing"
                class="flex flex-col items-center justify-center py-8 text-sm text-text-muted"
              >
                <svg class="mb-3 h-6 w-6 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                <span>正在识别语音，请稍候...</span>
                <span class="mt-1 text-xs opacity-60">首次使用需下载模型，可能需要几分钟</span>
              </div>

              <div v-else-if="transcriptError" class="py-4 text-center text-sm text-red-400">
                {{ transcriptError }}
              </div>

              <div v-else-if="transcriptSegments.length > 0" class="max-h-72 overflow-y-auto">
                <div
                  v-for="(seg, i) in transcriptSegments"
                  :key="i"
                  class="flex gap-3 py-1.5 text-xs"
                >
                  <span class="shrink-0 font-mono text-text-muted opacity-60">{{ seg.time }}</span>
                  <span class="text-text-secondary leading-relaxed">{{ seg.text }}</span>
                </div>
              </div>

              <div v-else class="py-4 text-center text-sm text-text-muted">
                未识别到语音内容
              </div>
            </div>
          </Transition>
        </div>

        <!-- Download button -->
        <button
          @click="emit('download', video.formats[selectedFormat].format_id)"
          :disabled="downloading"
          class="cursor-pointer mt-6 flex w-full items-center justify-center gap-2.5 rounded-xl bg-accent py-3.5 text-base font-bold text-bg-primary transition-all duration-200 hover:bg-accent-hover disabled:opacity-60 disabled:cursor-not-allowed"
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
            下载中，请稍候...
          </template>
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
