<template>
  <div class="column full-height bg-white">
    <!-- Document Management Header - Fixed -->
    <div class="col-auto border-b border-gray-200 p-4 flex items-center justify-between">
      <h2 class="text-lg font-medium text-gray-900">Documents</h2>
      <div class="flex items-center space-x-2">
        <!-- Quick Create Dropdown -->
        <div class="relative" ref="quickCreateRef">
          <BaseButton 
            variant="primary" 
            size="sm" 
            @click="showQuickCreate = !showQuickCreate"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            Quick Create
          </BaseButton>
          
          <!-- Quick Create Menu -->
          <div 
            v-if="showQuickCreate" 
            class="absolute right-0 top-full mt-1 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-50"
          >
            <button
              v-for="template in documentTemplates"
              :key="template.type"
              @click="createQuickDocument(template.type)"
              class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              {{ template.label }}
            </button>
          </div>
        </div>
        
        <!-- Custom Document -->
        <BaseButton 
          variant="outline" 
          size="sm" 
          @click="showNewDocumentDialog = true"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          Custom
        </BaseButton>
      </div>
    </div>

    <!-- Documents List - Scrollable -->
    <div class="col">
      <q-scroll-area class="full-height">
        <!-- Pinned Documents -->
        <div v-if="pinnedDocuments.length > 0" class="border-b border-gray-100">
          <div class="px-4 py-2 bg-gray-50 text-xs font-medium text-gray-500 uppercase tracking-wider">
            Pinned Documents
          </div>
          <DocumentItem
            v-for="document in pinnedDocuments"
            :key="`pinned-${document.id}`"
            :document="document"
            :is-active="activeDocumentId === document.id"
            :is-editing="editingDocumentId === document.id"
            @edit="startEditing"
            @save="saveDocument"
            @cancel="cancelEditing"
            @delete="deleteDocument"
            @toggle-pin="togglePin"
            @toggle-expand="toggleExpand"
            @expand-to-window="openDocumentInWindow"
            @focus="setActiveDocument"
            :is-in-window="documentsInWindows.has(document.id)"
          />
        </div>

        <!-- Regular Documents -->
        <div>
          <div v-if="pinnedDocuments.length > 0" class="px-4 py-2 bg-gray-50 text-xs font-medium text-gray-500 uppercase tracking-wider">
            Documents
          </div>
          <DocumentItem
            v-for="document in unpinnedDocuments"
            :key="document.id"
            :document="document"
            :is-active="activeDocumentId === document.id"
            :is-editing="editingDocumentId === document.id"
            @edit="startEditing"
            @save="saveDocument"
            @cancel="cancelEditing"
            @delete="deleteDocument"
            @toggle-pin="togglePin"
            @toggle-expand="toggleExpand"
            @expand-to-window="openDocumentInWindow"
            @focus="setActiveDocument"
            :is-in-window="documentsInWindows.has(document.id)"
          />
        </div>

        <!-- Empty State -->
        <div v-if="documents.length === 0" class="p-8 text-center text-gray-500">
          <svg class="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <p class="text-lg font-medium mb-2">No documents yet</p>
          <p class="mb-4">Get started by creating your first document</p>
          <BaseButton variant="primary" @click="showNewDocumentDialog = true">
            Create Document
          </BaseButton>
        </div>
      </q-scroll-area>
    </div>

    <!-- New Document Dialog -->
    <div v-if="showNewDocumentDialog" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showNewDocumentDialog = false"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Create New Document
            </h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Document Title
                </label>
                <input
                  v-model="newDocumentForm.label"
                  type="text"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter document title..."
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Initial Content (Optional)
                </label>
                <textarea
                  v-model="newDocumentForm.text"
                  rows="4"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Start writing your document content..."
                ></textarea>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <BaseButton 
              variant="primary" 
              @click="createCustomDocument"
              :disabled="!newDocumentForm.label.trim()"
            >
              Create Document
            </BaseButton>
            <BaseButton 
              variant="outline" 
              @click="showNewDocumentDialog = false"
              class="mr-2"
            >
              Cancel
            </BaseButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useDocumentStore } from '../../../stores/document'
import { windowManager } from '../../../services/windowManager'
import BaseButton from '../../ui/BaseButton.vue'
import DocumentItem from './DocumentItem.vue'

// Props
const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
})

// Store
const documentStore = useDocumentStore()

// Refs
const quickCreateRef = ref(null)
const showQuickCreate = ref(false)
const showNewDocumentDialog = ref(false)
const editingDocumentId = ref(null)
const documentsInWindows = ref(new Set()) // Track documents opened in new windows

// Form data
const newDocumentForm = ref({
  label: '',
  text: ''
})

// Document templates for quick create
const documentTemplates = [
  { type: 'abstract', label: 'Abstract' },
  { type: 'introduction', label: 'Introduction' },
  { type: 'methods', label: 'Methods' },
  { type: 'results', label: 'Results' },
  { type: 'discussion', label: 'Discussion' },
  { type: 'conclusion', label: 'Conclusion' },
  { type: 'summary', label: 'Summary' },
  { type: 'main-idea', label: 'Main Idea' }
]

// Computed
const documents = computed(() => documentStore.documentsByProject(props.projectId))
const pinnedDocuments = computed(() => documentStore.pinnedDocuments(props.projectId))
const unpinnedDocuments = computed(() => documentStore.unpinnedDocuments(props.projectId))
const activeDocumentId = computed(() => documentStore.activeDocumentId)

// Methods
async function loadDocuments() {
  if (props.projectId) {
    await documentStore.fetchByProject(props.projectId)
  }
}

async function createQuickDocument(type) {
  showQuickCreate.value = false
  
  const result = await documentStore.createQuick(props.projectId, type)
  if (result.success) {
    // Auto-start editing the new document
    editingDocumentId.value = result.data.id
    documentStore.setActiveDocument(result.data.id)
  } else {
    console.error('Failed to create document:', result.error)
    console.error('Full error details:', result.fullError)
    // TODO: Show user-friendly error notification
  }
}

async function createCustomDocument() {
  if (!newDocumentForm.value.label.trim()) return
  
  const result = await documentStore.create({
    projectId: props.projectId,
    label: newDocumentForm.value.label,
    text: newDocumentForm.value.text || '# ' + newDocumentForm.value.label + '\n\nStart writing here...',
    type: 'markdown'
  })
  
  if (result.success) {
    showNewDocumentDialog.value = false
    newDocumentForm.value = { label: '', text: '' }
    
    // Auto-start editing the new document
    editingDocumentId.value = result.data.id
    documentStore.setActiveDocument(result.data.id)
  } else {
    console.error('Failed to create document:', result.error)
    // TODO: Show user-friendly error notification
  }
}

function startEditing(documentId) {
  editingDocumentId.value = documentId
  documentStore.setActiveDocument(documentId)
}

async function saveDocument(documentId, updates, cancelEditing = true) {
  const result = await documentStore.update(documentId, updates)
  if (result.success) {
    if (cancelEditing) {
      editingDocumentId.value = null
    }
  } else {
    console.error('Failed to save document:', result.error)
    // TODO: Show user-friendly error notification
  }
}

function cancelEditing() {
  editingDocumentId.value = null
}

async function deleteDocument(documentId) {
  if (confirm('Are you sure you want to delete this document? This action cannot be undone.')) {
    const result = await documentStore.delete(documentId)
    if (!result.success) {
      console.error('Failed to delete document:', result.error)
      // TODO: Show user-friendly error notification
    }
  }
}

async function togglePin(documentId) {
  const result = await documentStore.togglePin(documentId)
  if (!result.success) {
    console.error('Failed to toggle pin:', result.error)
  }
}

function toggleExpand() {
  // This will be handled by the DocumentItem component internally
}

function setActiveDocument(documentId) {
  documentStore.setActiveDocument(documentId)
}

async function openDocumentInWindow(documentId) {
  const document = documents.value.find(doc => doc.id === documentId)
  if (!document) {
    console.error('Document not found:', documentId)
    return
  }

  try {
    // Convert reactive document to plain object
    const plainDocument = JSON.parse(JSON.stringify(document))
    const window = windowManager.openDocumentWindow(plainDocument)
    if (window) {
      // Track that this document is opened in a window
      documentsInWindows.value.add(documentId)
      console.log('Document opened in new window:', document.label)
    } else {
      console.error('Failed to open document window')
    }
  } catch (error) {
    console.error('Error opening document in window:', error)
  }
}

// Close quick create dropdown when clicking outside
function handleClickOutside(event) {
  if (quickCreateRef.value && !quickCreateRef.value.contains(event.target)) {
    showQuickCreate.value = false
  }
}

// Watch for project changes
watch(() => props.projectId, (newProjectId) => {
  if (newProjectId) {
    loadDocuments()
  }
}, { immediate: true })

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  loadDocuments()
  
  // Set up window manager callbacks
  windowManager.on('windowClosed', (documentId) => {
    documentsInWindows.value.delete(documentId)
    console.log('Document window closed:', documentId)
  })
  
  windowManager.on('documentUpdated', async (documentId, updates) => {
    // Update document in store when changed from window
    const result = await documentStore.update(documentId, updates)
    if (!result.success) {
      console.error('Failed to update document from window:', result.error)
    }
  })
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  
  // Clean up window manager callbacks
  windowManager.off('windowClosed')
  windowManager.off('documentUpdated')
  
  // Close all open windows when component unmounts
  windowManager.closeAllWindows()
})
</script>

<style scoped>
/* Add any custom styles here */
</style>