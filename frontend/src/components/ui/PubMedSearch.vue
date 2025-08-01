<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="handleBackdropClick">
    <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden" @click.stop>
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div class="flex items-center">
          <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900">PubMed Search</h3>
            <p class="text-sm text-gray-600">Search for research articles from PubMed</p>
          </div>
        </div>
        <button @click="handleClose" class="text-gray-400 hover:text-gray-600 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Search Form -->
      <div class="p-6 border-b border-gray-200">
        <form @submit.prevent="performSearch" class="space-y-4">
          <div>
            <label for="searchQuery" class="block text-sm font-medium text-gray-700 mb-2">
              Search Query
            </label>
            <input
              id="searchQuery"
              v-model="searchQuery"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., machine learning healthcare, COVID-19 treatment, etc."
            />
          </div>
          
          <div>
            <label for="maxResults" class="block text-sm font-medium text-gray-700 mb-2">
              Max Results
            </label>
            <select
              id="maxResults"
              v-model="maxResults"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option :value="10">10 results</option>
              <option :value="20">20 results</option>
              <option :value="50">50 results</option>
            </select>
          </div>

          <div class="flex justify-end">
            <BaseButton 
              type="submit"
              variant="primary" 
              :disabled="searching || !searchQuery.trim()"
            >
              <svg v-if="searching" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              {{ searching ? 'Searching...' : 'Search PubMed' }}
            </BaseButton>
          </div>
        </form>
      </div>

      <!-- Results -->
      <div class="flex-1 overflow-auto" style="max-height: 60vh;">
        <!-- Loading State -->
        <div v-if="searching" class="flex items-center justify-center py-12">
          <div class="text-center">
            <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p class="text-gray-600">Searching PubMed...</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="p-6 text-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Search Error</h3>
          <p class="text-gray-600 mb-4">{{ error }}</p>
          <BaseButton variant="outline" @click="error = null">
            Try Again
          </BaseButton>
        </div>

        <!-- No Results -->
        <div v-else-if="searchResults.length === 0 && hasSearched" class="p-6 text-center">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No Results Found</h3>
          <p class="text-gray-600">Try different search terms or check your spelling.</p>
        </div>

        <!-- Results List -->
        <div v-else-if="searchResults.length > 0" class="p-6">
          <div class="mb-4">
            <p class="text-sm text-gray-600">Found {{ totalResults }} articles</p>
          </div>
          
          <div class="space-y-4">
            <div 
              v-for="article in searchResults" 
              :key="article.pubmed_id"
              class="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors cursor-pointer"
              @click="selectArticle(article)"
            >
              <div class="flex justify-between items-start mb-2">
                <h4 class="text-lg font-medium text-gray-900 flex-1 mr-4">
                  {{ article.title }}
                </h4>
                <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                  PMID: {{ article.pubmed_id }}
                </span>
              </div>
              
              <div class="text-sm text-gray-600 mb-2">
                <span v-if="article.authors" class="mr-4">
                  <strong>Authors:</strong> {{ truncateText(article.authors, 100) }}
                </span>
                <span v-if="article.journal" class="mr-4">
                  <strong>Journal:</strong> {{ article.journal }}
                </span>
                <span v-if="article.publication_date">
                  <strong>Date:</strong> {{ formatDate(article.publication_date) }}
                </span>
              </div>
              
              <div v-if="article.abstract" class="text-sm text-gray-700 mb-3">
                {{ truncateText(article.abstract, 200) }}
              </div>
              
              <div class="flex justify-between items-center">
                <div class="flex space-x-2">
                  <span v-if="article.doi" class="text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded">
                    DOI: {{ article.doi }}
                  </span>
                  <span v-if="article.keywords && article.keywords.length > 0" class="text-xs text-green-600 bg-green-50 px-2 py-1 rounded">
                    {{ article.keywords.slice(0, 3).join(', ') }}{{ article.keywords.length > 3 ? '...' : '' }}
                  </span>
                </div>
                
                <div class="flex space-x-2">
                  <BaseButton 
                    variant="outline" 
                    size="sm"
                    @click.stop="previewArticle(article)"
                  >
                    Preview
                  </BaseButton>
                  <BaseButton 
                    variant="primary" 
                    size="sm"
                    @click.stop="importArticle(article)"
                    :disabled="importing === article.pubmed_id"
                  >
                    {{ importing === article.pubmed_id ? 'Importing...' : 'Import' }}
                  </BaseButton>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Initial State -->
        <div v-else class="p-6 text-center">
          <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Search PubMed</h3>
          <p class="text-gray-600">Enter search terms above to find research articles</p>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
        <div class="text-sm text-gray-600">
          <span v-if="searchResults.length">{{ searchResults.length }} result{{ searchResults.length !== 1 ? 's' : '' }} found</span>
          <span v-else-if="hasSearched && !loading">No results found</span>
        </div>
        <div class="flex space-x-2">
          <button
            @click="handleClose"
            class="px-4 py-2 text-sm bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Article Preview Modal -->
  <PubMedPreview 
    :show="showPreview"
    :article="selectedArticle"
    @close="showPreview = false"
    @import="importArticle"
  />
</template>

<script setup>
import { ref } from 'vue'
import { useApiStore } from '../../stores/api'
import { useUserStore } from '../../stores/user'
import BaseButton from './BaseButton.vue'
import PubMedPreview from './PubMedPreview.vue'

defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'import-success'])

// Stores
const apiStore = useApiStore()
const userStore = useUserStore()

// State
const searchQuery = ref('')
const maxResults = ref(20)
const searching = ref(false)
const error = ref(null)
const searchResults = ref([])
const totalResults = ref(0)
const hasSearched = ref(false)
const importing = ref(null)
const showPreview = ref(false)
const selectedArticle = ref(null)

// Methods
const performSearch = async () => {
  if (!searchQuery.value.trim()) return
  
  searching.value = true
  error.value = null
  hasSearched.value = true
  
  try {
    const response = await apiStore.post(`/pubmed/search?token=${userStore.token}`, {
      query: searchQuery.value.trim(),
      max_results: maxResults.value
    })
    
    searchResults.value = response.articles || []
    totalResults.value = response.total_results || 0
  } catch (err) {
    console.error('PubMed search error:', err)
    error.value = err.response?.data?.detail || 'Failed to search PubMed. Please try again.'
    searchResults.value = []
    totalResults.value = 0
  } finally {
    searching.value = false
  }
}

const selectArticle = (article) => {
  selectedArticle.value = article
  showPreview.value = true
}

const previewArticle = (article) => {
  selectedArticle.value = article
  showPreview.value = true
}

const importArticle = async (article) => {
  importing.value = article.pubmed_id
  
  try {
    await apiStore.post(`/pubmed/import?token=${userStore.token}`, {
      pubmed_id: article.pubmed_id
    })
    
    emit('import-success', article)
    
    // Show success message
    alert(`Successfully imported: ${article.title}`)
    
  } catch (err) {
    console.error('Import error:', err)
    const errorMsg = err.response?.data?.detail || 'Failed to import article'
    alert(`Import failed: ${errorMsg}`)
  } finally {
    importing.value = null
  }
}

const handleClose = () => {
  emit('close')
}

const handleBackdropClick = () => {
  emit('close')
}

// Utility functions
const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString()
  } catch {
    return dateString
  }
}
</script>