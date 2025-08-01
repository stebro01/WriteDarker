<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>
      
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle max-w-4xl w-full">
        <!-- Header -->
        <div class="bg-white px-6 pt-6 pb-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                {{ media?.filename || media?.label || 'Media Preview' }}
              </h3>
              <p class="mt-1 text-sm text-gray-500">
                {{ media?.filetype || 'Unknown' }} • {{ formatFileSize(media?.filesize) }}
              </p>
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="openInNewWindow"
                class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
                Open in New Window
              </button>
              <button
                @click="$emit('close')"
                class="text-gray-400 hover:text-gray-600 focus:outline-none focus:text-gray-600"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Content -->
        <div class="bg-white px-6 py-4" style="max-height: 70vh; overflow-y: auto;">
          <!-- Image Preview -->
          <div v-if="isImage" class="flex justify-center">
            <img
              :src="mediaUrl"
              :alt="media?.filename || media?.label"
              class="max-w-full max-h-96 object-contain rounded-lg shadow-sm"
              @error="handleImageError"
              @load="handleImageLoad"
            />
          </div>
          
          <!-- Video Preview -->
          <div v-else-if="isVideo" class="flex justify-center">
            <video
              :src="mediaUrl"
              controls
              class="max-w-full max-h-96 rounded-lg shadow-sm"
              @error="handleMediaError"
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
              >
                Your browser does not support the audio tag.
              </audio>
            </div>
          </div>
          
          <!-- Loading State -->
          <div v-else-if="loading" class="text-center py-12">
            <div class="inline-flex items-center">
              <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
              Loading preview...
            </div>
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="text-center text-gray-500 py-12">
            <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <p class="text-lg font-medium mb-2">Preview Error</p>
            <p class="mb-4">Unable to load media preview. Click "Open in New Window" to view the file.</p>
          </div>
          
          <!-- Unsupported Type -->
          <div v-else class="text-center text-gray-500 py-12">
            <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
            </svg>
            <p class="text-lg font-medium mb-2">Preview Not Available</p>
            <p class="mb-4">This media type cannot be previewed. Click "Open in New Window" to view the file.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
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
  return `${apiStore.baseUrl}/media/${props.media.id}/file?token=${userStore.token}`
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
  window.open(`${apiStore.baseUrl}/media/${props.media.id}/file?token=${userStore.token}`, '_blank')
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
    loading.value = true
  }
}, { immediate: true })

watch(() => props.show, (show) => {
  if (show && props.media) {
    error.value = false
    loading.value = true
  }
})
</script>

<style scoped>
/* Add any additional styling here */
</style>