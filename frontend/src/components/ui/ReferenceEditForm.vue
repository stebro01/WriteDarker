<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" v-if="show" @click="closeModal">
    <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white" @click.stop>
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-bold text-gray-900">Edit Reference</h3>
        <button
          @click="closeModal"
          class="text-gray-400 hover:text-gray-600"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <div class="max-h-96 overflow-y-auto">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700">Title</label>
            <input
              id="title"
              v-model="formData.title"
              type="text"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>

          <div>
            <label for="authors" class="block text-sm font-medium text-gray-700">Authors</label>
            <input
              id="authors"
              v-model="formData.authors"
              type="text"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label for="journal" class="block text-sm font-medium text-gray-700">Journal</label>
            <input
              id="journal"
              v-model="formData.journal"
              type="text"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label for="year" class="block text-sm font-medium text-gray-700">Year</label>
            <input
              id="year"
              v-model="formData.year"
              type="text"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label for="doi" class="block text-sm font-medium text-gray-700">DOI</label>
            <input
              id="doi"
              v-model="formData.doi"
              type="text"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label for="url" class="block text-sm font-medium text-gray-700">URL</label>
            <input
              id="url"
              v-model="formData.url"
              type="url"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label for="keywords" class="block text-sm font-medium text-gray-700">Keywords</label>
            <input
              id="keywords"
              v-model="formData.keywords"
              type="text"
              placeholder="Comma-separated keywords"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label for="publication_date" class="block text-sm font-medium text-gray-700">Publication Date</label>
            <input
              id="publication_date"
              v-model="formData.publication_date"
              type="text"
              placeholder="YYYY-MM-DD or YYYY/MM/DD"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label for="abstract" class="block text-sm font-medium text-gray-700">Abstract</label>
            <textarea
              id="abstract"
              v-model="formData.abstract"
              rows="4"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            ></textarea>
          </div>

          <div>
            <label for="citation" class="block text-sm font-medium text-gray-700">Citation</label>
            <textarea
              id="citation"
              v-model="formData.citation"
              rows="2"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            ></textarea>
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="px-4 py-2 bg-blue-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {{ loading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Error display -->
      <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useReferenceStore } from '../../stores/reference'

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

function closeModal() {
  error.value = ''
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
      closeModal()
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