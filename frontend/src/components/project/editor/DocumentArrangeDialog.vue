<template>
  <BaseModal
    :show="show"
    @close="handleClose"
    title="Arrange Documents"
    subtitle="Drag and drop to reorder your documents"
    size="lg"
  >
    <div class="space-y-4">
      <!-- Instructions -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div class="flex items-start">
          <svg class="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <div>
            <h4 class="text-sm font-medium text-blue-900 mb-1">How to arrange</h4>
            <p class="text-sm text-blue-800">
              Drag and drop documents to reorder them. The new order will be saved automatically when you close this dialog.
            </p>
          </div>
        </div>
      </div>

      <!-- Document List for Reordering -->
      <div class="space-y-2 max-h-96 overflow-y-auto">
        <draggable
          v-model="localDocuments"
          group="documents"
          :animation="200"
          handle=".drag-handle"
          ghost-class="ghost"
          chosen-class="chosen"
          drag-class="drag"
          @end="onDragEnd"
          item-key="id"
        >
          <template #item="{ element: document, index }">
            <div class="bg-white border border-gray-200 rounded-lg p-4 flex items-center space-x-3 hover:bg-gray-50 transition-colors">
              <!-- Drag Handle -->
              <div class="drag-handle cursor-move text-gray-400 hover:text-gray-600">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>
                </svg>
              </div>
              
              <!-- Order Number -->
              <div class="flex-shrink-0 w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center text-sm font-medium text-gray-600">
                {{ index + 1 }}
              </div>
              
              <!-- Document Info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2">
                  <!-- Pin Icon -->
                  <svg v-if="document.isPinned" class="w-4 h-4 text-orange-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 5V3h10v2L9 8v7l1 1v1H8v-1l1-1V8L5 5z"/>
                  </svg>
                  
                  <!-- Document Title -->
                  <h3 class="text-sm font-medium text-gray-900 truncate">
                    {{ document.label }}
                  </h3>
                </div>
                
                <!-- Document Meta -->
                <div class="flex items-center space-x-2 mt-1">
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                    {{ document.type || 'markdown' }}
                  </span>
                  <span class="text-xs text-gray-500">
                    {{ formatDate(document.updatedAt) }}
                  </span>
                </div>
              </div>
              
              <!-- Status Indicators -->
              <div class="flex items-center space-x-2">
                <!-- In Window Indicator -->
                <div v-if="isInWindow(document.id)" class="flex items-center text-xs text-blue-600">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                  </svg>
                  Window
                </div>
                
                <!-- Active Indicator -->
                <div v-if="document.id === activeDocumentId" class="w-2 h-2 bg-orange-500 rounded-full"></div>
              </div>
            </div>
          </template>
        </draggable>
      </div>
      
      <!-- Empty State -->
      <div v-if="localDocuments.length === 0" class="text-center py-8 text-gray-500">
        <svg class="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <p>No documents to arrange</p>
      </div>
    </div>
    
    <template #footer>
      <BaseButton 
        variant="outline" 
        @click="handleClose"
      >
        Cancel
      </BaseButton>
      <BaseButton 
        variant="primary" 
        @click="saveOrder"
        :disabled="!hasChanges"
      >
        Save Order
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import draggable from 'vuedraggable'
import BaseModal from '../../ui/BaseModal.vue'
import BaseButton from '../../ui/BaseButton.vue'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  documents: {
    type: Array,
    default: () => []
  },
  activeDocumentId: {
    type: Number,
    default: null
  },
  documentsInWindows: {
    type: Set,
    default: () => new Set()
  }
})

// Emits
const emit = defineEmits(['close', 'save-order'])

// Reactive data
const localDocuments = ref([])
const originalOrder = ref([])

// Computed
const hasChanges = computed(() => {
  if (localDocuments.value.length !== originalOrder.value.length) return true
  
  return localDocuments.value.some((doc, index) => {
    return doc.id !== originalOrder.value[index]?.id
  })
})

// Methods
function initializeDocuments() {
  // Create a copy of documents with current order
  localDocuments.value = [...props.documents].map(doc => ({ ...doc }))
  originalOrder.value = localDocuments.value.map(doc => ({ id: doc.id }))
}

function onDragEnd() {
  // This is called after drag ends, localDocuments is already updated by vuedraggable
  console.log('Drag ended, new order:', localDocuments.value.map(d => d.label))
}

function isInWindow(documentId) {
  return props.documentsInWindows.has(documentId)
}

function formatDate(dateString) {
  if (!dateString) return 'Unknown'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: date.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
    })
  } catch {
    return 'Invalid date'
  }
}

function handleClose() {
  emit('close')
}

function saveOrder() {
  if (hasChanges.value) {
    // Emit the new order as an array of document IDs
    const newOrder = localDocuments.value.map(doc => doc.id)
    emit('save-order', newOrder)
  }
  emit('close')
}

// Watch for prop changes
watch(() => props.show, (newShow) => {
  if (newShow) {
    initializeDocuments()
  }
})

watch(() => props.documents, () => {
  if (props.show) {
    initializeDocuments()
  }
}, { deep: true })
</script>

<style scoped>
.ghost {
  opacity: 0.5;
  background-color: #f3f4f6;
  border: 2px dashed #d1d5db;
}

.chosen {
  opacity: 0.8;
}

.drag {
  transform: rotate(5deg);
}

.drag-handle:hover {
  cursor: grab;
}

.drag-handle:active {
  cursor: grabbing;
}
</style>