<template>
  <BaseModal
    :show="show"
    @close="$emit('')"
    :title="media?.filename || media?.label || 'Media Preview'"
    :subtitle="media?.filetype || media?.filesize ? `${media?.filetype || 'Unknown'}${media?.filesize ? ' • ' + formatFileSize(media.filesize) : ''}` : ''"
    size="xl"
  >
    <div class="space-y-4">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center h-64">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="flex items-center justify-center h-64">
          <div class="text-center">
            <svg class="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-gray-600">Unable to load media preview</p>
          </div>
        </div>

        <!-- Image Preview -->
        <div v-else-if="isImage" class="flex justify-center">
          <img 
            :src="mediaUrl" 
            :alt="media?.filename || media?.label"
            class="max-w-full max-h-96 object-contain rounded"
            @error="handleImageError"
            @load="handleImageLoad"
            @loadstart="loading = true"
          />
        </div>
          
        <!-- Video Preview -->
        <div v-else-if="isVideo" class="flex justify-center">
          <video
            :src="mediaUrl"
            controls
            class="max-w-full max-h-96 rounded"
            @error="handleMediaError"
            @loadstart="loading = true"
            @loadeddata="loading = false"
          >
            Your browser does not support the video tag.
          </video>
        </div>
          
        <!-- Audio Preview -->
        <div v-else-if="isAudio" class="flex justify-center">
          <div class="w-full max-w-md">
            <div class="text-center mb-4">
              <svg class="w-16 h-16 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/>
              </svg>
            </div>
            <audio
              :src="mediaUrl"
              controls
              class="w-full"
              @error="handleMediaError"
              @loadstart="loading = true"
              @loadeddata="loading = false"
            >
              Your browser does not support the audio tag.
            </audio>
          </div>
        </div>
        
        <!-- Unsupported Type -->
        <div v-else class="flex items-center justify-center h-64">
          <div class="text-center">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
            </svg>
            <p class="text-gray-600">Preview not available for this file type</p>
          </div>
        </div>
    </div>

    <template #footer>
      <BaseButton
        @click="openInNewWindow"
        class="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        <svg class="w-4 h-4 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
        </svg>
        Open
      </BaseButton>

    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import BaseModal from './BaseModal.vue'
import BaseButton from './BaseButton.vue'
import { useApiStore } from '../../stores/api'
import { useUserStore } from '../../stores/user'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  media: {
    type: Object,
    default: null
  }
})

// Emits
defineEmits(['close'])

// Stores
const apiStore = useApiStore()
const userStore = useUserStore()

// State
const loading = ref(false)
const error = ref(false)

// Computed
const mediaUrl = computed(() => {
  if (!props.media?.id) return ''
  return `${apiStore.baseUrl}/documents/${props.media.id}/file?token=${userStore.token}`
})

const isImage = computed(() => {
  const type = props.media?.filetype?.toLowerCase() || ''
  const filename = props.media?.filename?.toLowerCase() || ''
  return type.startsWith('image/') || 
         filename.match(/\.(jpg|jpeg|png|gif|bmp|webp|svg)$/)
})

const isVideo = computed(() => {
  const type = props.media?.filetype?.toLowerCase() || ''
  const filename = props.media?.filename?.toLowerCase() || ''
  return type.startsWith('video/') || 
         filename.match(/\.(mp4|avi|mov|wmv|flv|webm|mkv)$/)
})

const isAudio = computed(() => {
  const type = props.media?.filetype?.toLowerCase() || ''
  const filename = props.media?.filename?.toLowerCase() || ''
  return type.startsWith('audio/') || 
         filename.match(/\.(mp3|wav|ogg|aac|flac|m4a)$/)
})

// Methods
function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  if (!bytes) return ''
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

function openInNewWindow() {
  if (!props.media?.id) return
  window.open(`${apiStore.baseUrl}/documents/${props.media.id}/file?token=${userStore.token}`, '_blank')
}

function handleImageError() {
  error.value = true
  loading.value = false
}

function handleImageLoad() {
  loading.value = false
  error.value = false
}

function handleMediaError() {
  error.value = true
  loading.value = false
}

// Watch for media changes
watch(() => props.media, (newMedia) => {
  if (newMedia && props.show) {
    error.value = false
    loading.value = false
  }
}, { immediate: true })

watch(() => props.show, (show) => {
  if (show && props.media) {
    error.value = false
    loading.value = false
  }
})
</script>

<style scoped>
/* Add any additional styling here */
</style>