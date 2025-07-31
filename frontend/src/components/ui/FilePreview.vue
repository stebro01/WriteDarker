<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="closePreview">
    <div class="bg-white rounded-lg shadow-xl max-w-4xl max-h-[90vh] w-full mx-4 flex flex-col" @click.stop>
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">{{ reference?.title || 'Preview' }}</h3>
          <p v-if="reference && reference.filename !== reference.title" class="text-sm text-gray-600">{{ reference?.filename || 'No filename' }}</p>
        </div>
        <button @click="closePreview" class="text-gray-400 hover:text-gray-600 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Content Area -->
      <div class="flex-1 overflow-auto p-4">
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
            <p class="text-gray-600">{{ error }}</p>
          </div>
        </div>

        <!-- PDF Preview -->
        <div v-else-if="fileType === 'pdf'" class="h-96">
          <iframe 
            :src="fileUrl" 
            class="w-full h-full border rounded"
            title="PDF Preview"
          ></iframe>
        </div>

        <!-- Image Preview -->
        <div v-else-if="fileType === 'image'" class="flex justify-center">
          <img 
            :src="fileUrl" 
            :alt="reference?.filename"
            class="max-w-full max-h-96 object-contain rounded"
          />
        </div>

        <!-- Text Preview -->
        <div v-else-if="fileType === 'text'" class="bg-gray-50 rounded p-4 max-h-96 overflow-auto">
          <pre class="whitespace-pre-wrap text-sm font-mono">{{ textContent }}</pre>
        </div>

        <!-- JSON Preview -->
        <div v-else-if="fileType === 'json'" class="bg-gray-50 rounded p-4 max-h-96 overflow-auto">
          <pre class="whitespace-pre-wrap text-sm font-mono">{{ formattedJson }}</pre>
        </div>

        <!-- Unsupported File Type -->
        <div v-else class="flex items-center justify-center h-64">
          <div class="text-center">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <p class="text-gray-600 mb-2">Preview not available</p>
            <p class="text-sm text-gray-500">{{ reference?.filetype || 'Unknown file type' }}</p>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between p-4 border-t bg-gray-50">
        <div class="text-sm text-gray-600">
          <span v-if="reference?.filetype">{{ reference.filetype }}</span>
          <span v-if="reference?.authors" class="ml-4">{{ reference.authors }}</span>
        </div>
        <div class="flex space-x-2">
          <button
            v-if="fileUrl"
            @click="downloadFile"
            class="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            Download
          </button>
          <button
            @click="closePreview"
            class="px-4 py-2 text-sm bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useUserStore } from '../../stores/user'

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

const emit = defineEmits(['close'])

const userStore = useUserStore()
const loading = ref(false)
const error = ref(null)
const fileUrl = ref(null)
const textContent = ref('')

const fileType = computed(() => {
  if (!props.reference?.filetype) return null
  
  const type = props.reference.filetype.toLowerCase()
  
  if (type.includes('pdf')) return 'pdf'
  if (type.includes('image') || type.includes('png') || type.includes('jpg') || type.includes('jpeg') || type.includes('gif') || type.includes('webp')) return 'image'
  if (type.includes('text') || type.includes('plain')) return 'text'
  if (type.includes('json')) return 'json'
  
  // Check by filename extension if filetype is not clear
  const filename = props.reference?.filename?.toLowerCase() || ''
  if (filename.endsWith('.pdf')) return 'pdf'
  if (filename.endsWith('.png') || filename.endsWith('.jpg') || filename.endsWith('.jpeg') || filename.endsWith('.gif') || filename.endsWith('.webp')) return 'image'
  if (filename.endsWith('.txt') || filename.endsWith('.dat')) return 'text'
  if (filename.endsWith('.json')) return 'json'
  
  return null
})

const formattedJson = computed(() => {
  if (fileType.value === 'json' && textContent.value) {
    try {
      const parsed = JSON.parse(textContent.value)
      return JSON.stringify(parsed, null, 2)
    } catch {
      return textContent.value
    }
  }
  return ''
})

const closePreview = () => {
  emit('close')
  // Clean up resources
  if (fileUrl.value && fileUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(fileUrl.value)
  }
  fileUrl.value = null
  textContent.value = ''
  error.value = null
}

const downloadFile = () => {
  if (fileUrl.value) {
    const a = document.createElement('a')
    a.href = fileUrl.value
    a.download = props.reference?.filename || 'download'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }
}

const loadFileContent = async () => {
  if (!props.reference?.id || !props.show) return
  
  // Don't try to load file content for PubMed articles without files
  if (props.reference.pubmed_id && !props.reference.filename) {
    error.value = 'This is a PubMed article without an associated file. Use the "View" button to see article details.'
    loading.value = false
    return
  }
  
  // Don't try to load if there's no file
  if (!props.reference.filename) {
    error.value = 'No file available for preview'
    loading.value = false
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    // Fetch the file content from the API
    const response = await fetch(`http://localhost:8000/references/${props.reference.id}/file?token=${userStore.token}`)
    
    if (!response.ok) {
      throw new Error(`Failed to load file: ${response.statusText}`)
    }
    
    const blob = await response.blob()
    
    if (fileType.value === 'text' || fileType.value === 'json') {
      // For text files, read as text
      textContent.value = await blob.text()
    } else {
      // For binary files (PDF, images), create object URL
      fileUrl.value = URL.createObjectURL(blob)
    }
    
  } catch (err) {
    console.error('Error loading file:', err)
    error.value = err.message || 'Failed to load file'
  } finally {
    loading.value = false
  }
}

// Watch for changes in show prop and reference
watch([() => props.show, () => props.reference], ([newShow, newRef]) => {
  if (newShow && newRef) {
    loadFileContent()
  } else if (!newShow) {
    closePreview()
  }
}, { immediate: true })
</script>