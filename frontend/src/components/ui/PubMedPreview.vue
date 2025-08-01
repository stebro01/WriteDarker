<template>
  <BaseModal
    :show="show && !!article"
    @close="handleClose"
    title="Article Preview"
    :subtitle="`PMID: ${article?.pubmed_id || 'N/A'}`"
    size="xl"
  >
    <template #header>
      <div class="flex items-center">
        <div class="w-10 h-10 bg-gradient-to-r from-green-500 to-green-600 rounded-full flex items-center justify-center mr-3">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-semibold text-gray-900">Article Preview</h3>
          <p class="text-sm text-gray-600 mt-1">PMID: {{ article?.pubmed_id || 'N/A' }}</p>
        </div>
      </div>
    </template>

    <div class="space-y-6">
        <!-- Title -->
        <div class="mb-6">
          <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ article.title }}</h1>
          
          <!-- Metadata -->
          <div class="flex flex-wrap gap-4 text-sm text-gray-600 mb-4">
            <span v-if="article.authors" class="flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              <strong>Authors:</strong> {{ article.authors }}
            </span>
            
            <span v-if="article.journal" class="flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
              <strong>Journal:</strong> {{ article.journal }}
            </span>
            
            <span v-if="article.publication_date" class="flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              <strong>Date:</strong> {{ formatDate(article.publication_date) }}
            </span>
          </div>

          <!-- Tags -->
          <div class="flex flex-wrap gap-2 mb-4">
            <span v-if="article.doi" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
              </svg>
              DOI: {{ article.doi }}
            </span>
            
            <template v-if="article.keywords && article.keywords.length > 0">
              <span v-for="keyword in article.keywords.slice(0, 5)" 
                    :key="keyword"
                    class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                {{ keyword }}
              </span>
            </template>
            
            <span v-if="article.keywords && article.keywords.length > 5" 
                  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
              +{{ article.keywords.length - 5 }} more
            </span>
          </div>
        </div>

        <!-- Abstract -->
        <div v-if="article.abstract" class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-3 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Abstract
          </h2>
          <div class="prose prose-sm max-w-none">
            <p class="text-gray-700 leading-relaxed">{{ article.abstract }}</p>
          </div>
        </div>

        <!-- Citation -->
        <div v-if="article.citation" class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-3 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path>
            </svg>
            Citation
          </h2>
          <div class="bg-gray-50 rounded-lg p-4">
            <p class="text-sm text-gray-700 font-mono">{{ article.citation }}</p>
            <button 
              @click="copyCitation"
              class="mt-2 text-xs text-blue-600 hover:text-blue-800 flex items-center"
            >
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
              </svg>
              Copy Citation
            </button>
          </div>
        </div>

        <!-- Links -->
        <div class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-3 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
            </svg>
            External Links
          </h2>
          <div class="space-y-2">
            <a 
              v-if="article.url" 
              :href="article.url" 
              target="_blank" 
              rel="noopener noreferrer"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
              </svg>
              View on PubMed
            </a>
            
            <a 
              v-if="article.doi" 
              :href="`https://doi.org/${article.doi}`" 
              target="_blank" 
              rel="noopener noreferrer"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors ml-2"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
              </svg>
              View DOI
            </a>
          </div>
        </div>

        <!-- Link to Existing Reference -->
        <div v-if="availableReferences.length > 0" class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-3 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
            </svg>
            Link to Existing PDF
          </h2>
          <p class="text-sm text-gray-600 mb-3">
            You can link this PubMed article's metadata to an existing PDF in your library:
          </p>
          <div class="space-y-2">
            <div 
              v-for="ref in availableReferences" 
              :key="ref.id"
              class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:border-blue-300 transition-colors"
            >
              <div class="flex-1">
                <h4 class="font-medium text-gray-900">{{ ref.title }}</h4>
                <p class="text-sm text-gray-600">{{ ref.filename }}</p>
              </div>
              <BaseButton 
                variant="outline" 
                size="sm"
                @click="linkToReference(ref)"
                :disabled="linking === ref.id"
              >
                {{ linking === ref.id ? 'Linking...' : 'Link' }}
              </BaseButton>
            </div>
          </div>
        </div>
    </div>

    <template #footer>
      <BaseButton variant="outline" @click="handleClose">
        Close
      </BaseButton>
      <BaseButton 
        variant="primary" 
        @click="importArticle"
        :disabled="importing"
      >
        <svg v-if="importing" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        {{ importing ? 'Importing...' : 'Import to Library' }}
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BaseModal from './BaseModal.vue'
import BaseButton from './BaseButton.vue'
import { useApiStore } from '../../stores/api'
import { useUserStore } from '../../stores/user'
import { useReferenceStore } from '../../stores/reference'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  article: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'import'])

// Stores
const apiStore = useApiStore()
const userStore = useUserStore()
const referenceStore = useReferenceStore()

// State
const importing = ref(false)
const linking = ref(null)

// Computed
const availableReferences = computed(() => {
  return referenceStore.references.filter(ref => 
    ref.filename && 
    (ref.filename.toLowerCase().endsWith('.pdf') || ref.filetype?.includes('pdf')) &&
    !ref.pubmed_id // Only show references without PubMed metadata
  )
})

// Methods
const handleClose = () => {
  emit('close')
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  } catch {
    return dateString
  }
}

const copyCitation = async () => {
  if (!props.article?.citation) return
  
  try {
    await navigator.clipboard.writeText(props.article.citation)
    alert('Citation copied to clipboard!')
  } catch (err) {
    console.error('Failed to copy citation:', err)
    // Fallback for browsers that don't support clipboard API
    const textArea = document.createElement('textarea')
    textArea.value = props.article.citation
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    alert('Citation copied to clipboard!')
  }
}

const importArticle = async () => {
  if (!props.article) return
  
  importing.value = true
  try {
    emit('import', props.article)
  } finally {
    importing.value = false
  }
}

const linkToReference = async (reference) => {
  if (!props.article) return
  
  linking.value = reference.id
  try {
    await apiStore.post(`/pubmed/import?token=${userStore.token}`, {
      pubmed_id: props.article.pubmed_id,
      link_to_reference_id: reference.id
    })
    
    // Refresh references to show updated metadata
    await referenceStore.fetchAll()
    
    alert(`Successfully linked PubMed metadata to "${reference.title}"`)
    emit('close')
    
  } catch (err) {
    console.error('Link error:', err)
    const errorMsg = err.response?.data?.detail || 'Failed to link article'
    alert(`Link failed: ${errorMsg}`)
  } finally {
    linking.value = null
  }
}

// Load references when component mounts
onMounted(() => {
  if (props.show && referenceStore.references.length === 0) {
    referenceStore.fetchAll()
  }
})
</script>