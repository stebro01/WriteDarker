<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="handleBackdropClick">
    <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden" @click.stop>
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div class="flex items-center">
          <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900">Edit Reference</h3>
            <p class="text-sm text-gray-600">{{ reference?.title || 'Update reference details' }}</p>
          </div>
        </div>
        <button @click="handleClose" class="text-gray-400 hover:text-gray-600 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-auto p-6" style="max-height: 70vh;">
        <!-- Error display -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="text-red-800">{{ error }}</span>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Basic Information Section -->
          <div>
            <h4 class="text-base font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Basic Information
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title *</label>
                <input
                  id="title"
                  v-model="formData.title"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label for="authors" class="block text-sm font-medium text-gray-700 mb-1">Authors</label>
                <input
                  id="authors"
                  v-model="formData.authors"
                  type="text"
                  placeholder="e.g., Smith J, Doe A"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label for="journal" class="block text-sm font-medium text-gray-700 mb-1">Journal</label>
                <input
                  id="journal"
                  v-model="formData.journal"
                  type="text"
                  placeholder="Journal name"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label for="year" class="block text-sm font-medium text-gray-700 mb-1">Year</label>
                <input
                  id="year"
                  v-model="formData.year"
                  type="text"
                  placeholder="e.g., 2024"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>

          <!-- Publication Details Section -->
          <div>
            <h4 class="text-base font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
              Publication Details
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="doi" class="block text-sm font-medium text-gray-700 mb-1">DOI</label>
                <input
                  id="doi"
                  v-model="formData.doi"
                  type="text"
                  placeholder="e.g., 10.1000/123456"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label for="url" class="block text-sm font-medium text-gray-700 mb-1">URL</label>
                <input
                  id="url"
                  v-model="formData.url"
                  type="url"
                  placeholder="https://example.com"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label for="publication_date" class="block text-sm font-medium text-gray-700 mb-1">Publication Date</label>
                <input
                  id="publication_date"
                  v-model="formData.publication_date"
                  type="text"
                  placeholder="YYYY-MM-DD or YYYY/MM/DD"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label for="keywords" class="block text-sm font-medium text-gray-700 mb-1">Keywords</label>
                <input
                  id="keywords"
                  v-model="formData.keywords"
                  type="text"
                  placeholder="Comma-separated keywords"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>

          <!-- Content Section -->
          <div>
            <h4 class="text-base font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              Content
            </h4>
            <div class="space-y-4">
              <div>
                <label for="abstract" class="block text-sm font-medium text-gray-700 mb-1">Abstract</label>
                <textarea
                  id="abstract"
                  v-model="formData.abstract"
                  rows="4"
                  placeholder="Enter the abstract or summary of the reference..."
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
                ></textarea>
              </div>

              <div>
                <label for="citation" class="block text-sm font-medium text-gray-700 mb-1">Citation</label>
                <textarea
                  id="citation"
                  v-model="formData.citation"
                  rows="2"
                  placeholder="Formatted citation (e.g., APA, MLA, Chicago style)..."
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
                ></textarea>
              </div>
            </div>
          </div>
        </form>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between p-6 border-t border-gray-200">
        <div class="text-sm text-gray-500">
          <span v-if="reference?.filename">File: {{ reference.filename }}</span>
          <span v-else-if="reference?.pubmed_id">PubMed ID: {{ reference.pubmed_id }}</span>
        </div>
        <div class="flex space-x-3">
          <BaseButton variant="outline" @click="handleClose">
            Cancel
          </BaseButton>
          <BaseButton 
            variant="primary" 
            @click="handleSubmit"
            :loading="loading"
            :disabled="loading"
          >
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useReferenceStore } from '../../stores/reference'
import BaseButton from './BaseButton.vue'

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

const emit = defineEmits(['close', 'updated'])

const referenceStore = useReferenceStore()
const loading = ref(false)
const error = ref('')

const formData = ref({
  title: '',
  authors: '',
  journal: '',
  year: '',
  doi: '',
  url: '',
  keywords: '',
  publication_date: '',
  abstract: '',
  citation: ''
})

// Watch for reference changes to populate the form
watch(() => props.reference, (newReference) => {
  if (newReference) {
    formData.value = {
      title: newReference.title || '',
      authors: newReference.authors || '',
      journal: newReference.journal || '',
      year: newReference.year || '',
      doi: newReference.doi || '',
      url: newReference.url || '',
      keywords: newReference.keywords || '',
      publication_date: newReference.publication_date || '',
      abstract: newReference.abstract || '',
      citation: newReference.citation || ''
    }
  }
}, { immediate: true })

function handleClose() {
  error.value = ''
  emit('close')
}

function handleBackdropClick() {
  emit('close')
}

async function handleSubmit() {
  if (!props.reference) return
  
  loading.value = true
  error.value = ''
  
  try {
    // Only send fields that have been modified
    const updateData = {}
    
    // Include all fields that might have changed
    Object.keys(formData.value).forEach(key => {
      const value = formData.value[key]
      if (value !== null && value !== undefined) {
        updateData[key] = value === '' ? null : value
      }
    })
    
    const result = await referenceStore.update(props.reference.id, updateData)
    
    if (result.success) {
      emit('updated', result.data)
      handleClose()
    } else {
      error.value = result.error || 'Failed to update reference'
    }
  } catch (err) {
    error.value = err.message || 'An error occurred while updating the reference'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.resize-vertical {
  resize: vertical;
}
</style>