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
                {{ reference?.filename || reference?.title || 'Reference Preview' }}
              </h3>
              <p class="mt-1 text-sm text-gray-500">
                {{ reference?.filetype || 'Unknown' }} • {{ formatFileSize(reference?.filesize) }}
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
          <!-- PDF Preview -->
          <div v-if="isPdf" class="w-full">
            <div class="text-center text-gray-500 py-12">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <p class="text-lg font-medium mb-2">PDF Preview</p>
              <p class="mb-4">Click "Open in New Window" to view the full PDF document</p>
            </div>
          </div>
          
          <!-- Text/Other Preview -->
          <div v-else-if="referenceContent" class="prose max-w-none">
            <pre class="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded-lg">{{ referenceContent }}</pre>
          </div>
          
          <!-- Loading State -->
          <div v-else-if="loading" class="text-center py-12">
            <div class="inline-flex items-center">
              <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
              Loading preview...
            </div>
          </div>
          
          <!-- Error State -->
          <div v-else class="text-center text-gray-500 py-12">
            <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <p class="text-lg font-medium mb-2">Preview Not Available</p>
            <p class="mb-4">This file type cannot be previewed. Click "Open in New Window" to view the file.</p>
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
  reference: {
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
const referenceContent = ref('')

// Computed
const isPdf = computed(() => {
  return props.reference?.filetype?.toLowerCase() === 'pdf' || 
         props.reference?.filename?.toLowerCase().endsWith('.pdf')
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
  if (!props.reference?.id) return
  window.open(`${apiStore.baseUrl}/references/${props.reference.id}/file?token=${userStore.token}`, '_blank')
}

async function loadPreview() {
  if (!props.reference?.id || isPdf.value) return
  
  loading.value = true
  referenceContent.value = ''
  
  try {
    // For text files, we could try to fetch and preview content
    // For now, we'll just show that preview is not available for most files
    // In a real implementation, you might have an API endpoint for text preview
    loading.value = false
  } catch (error) {
    console.error('Failed to load reference preview:', error)
    loading.value = false
  }
}

// Watch for reference changes
watch(() => props.reference, (newReference) => {
  if (newReference && props.show) {
    loadPreview()
  }
}, { immediate: true })

watch(() => props.show, (show) => {
  if (show && props.reference) {
    loadPreview()
  }
})
</script>

<style scoped>
/* Add any additional styling here */
</style>