<template>
  <div 
    :class="[
      'bg-white border-r border-gray-200 flex flex-col transition-all duration-300',
      collapsed ? 'w-12' : 'w-80 sm:w-72 lg:w-80'
    ]"
  >
    <!-- Sidebar header -->
    <div class="p-3 border-b border-gray-200 flex items-center justify-between">
      <div v-if="!collapsed" class="text-xs font-medium text-gray-600 uppercase tracking-wide">References & Files</div>
      <button
        @click="$emit('toggle-collapse')"
        class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="collapsed ? 'M9 5l7 7-7 7' : 'M15 19l-7-7 7-7'"></path>
        </svg>
      </button>
    </div>

    <!-- Sidebar content -->
    <div v-if="!collapsed" class="column flex-1 overflow-y-auto min-h-0 sidebar-scrollable">
      <!-- Add Files Button -->
      <div class="col-auto q-pa-sm">
        <q-btn
          :disable="!projectId || isNewProject"
          @click="handleAddFilesClick"
          outline
          color="orange-6"
          size="sm"
          class="full-width q-py-sm"
          icon="add"
        >
          <span class="q-ml-xs">{{ (!projectId || isNewProject) ? 'Save project first' : 'Add Files' }}</span>
        </q-btn>
      </div>

      <!-- References and Media Files List -->
      <div class="col">
        <q-list dense class="q-pa-none">
          <ReferenceList
            v-model:expanded="referencesExpanded"
            :references="references"
            @add="$emit('show-reference-search')"
            @select="openReference"
            @preview="previewReference"
            @open-in-window="openReferenceInWindow"
          />
          <MediaList
            v-model:expanded="mediaFilesExpanded"
            :media="mediaFiles"
            @select="$emit('edit-media', $event)"
            @delete="deleteMedia"
            @preview="previewMedia"
            @open-in-window="openMediaInWindow"
          />
        </q-list>
      </div>
    </div>

    <!-- Collapsed sidebar icons -->
    <div v-else class="flex-1 flex flex-col items-center py-2 sm:py-4 space-y-2 sm:space-y-3 overflow-y-auto min-h-0">
      <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
      </button>
      <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ReferenceList from '../ReferenceList.vue'
import MediaList from '../MediaList.vue'
import { useApiStore } from '../../../stores/api'
import { useUserStore } from '../../../stores/user'
import { useMediaStore } from '../../../stores/media'

// Props
defineProps({
  collapsed: {
    type: Boolean,
    default: false
  },
  projectId: {
    type: Number,
    default: null
  },
  isNewProject: {
    type: Boolean,
    default: false
  },
  references: {
    type: Array,
    default: () => []
  },
  mediaFiles: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits([
  'toggle-collapse',
  'show-file-action',
  'show-reference-search',
  'edit-media',
  'preview-reference',
  'preview-media'
])

// Stores
const apiStore = useApiStore()
const userStore = useUserStore()
const mediaStore = useMediaStore()

// Local state
const referencesExpanded = ref(true)
const mediaFilesExpanded = ref(true)

// Methods
function handleAddFilesClick() {
  emit('show-file-action')
}

function openReference(ref) {
  if (!ref?.id) return
  window.open(`${apiStore.baseUrl}/references/${ref.id}/file?token=${userStore.token}`, '_blank')
}

function previewReference(reference) {
  emit('preview-reference', reference)
}

function openReferenceInWindow(reference) {
  if (!reference?.id) return
  window.open(`${apiStore.baseUrl}/references/${reference.id}/file?token=${userStore.token}`, '_blank')
}

function previewMedia(media) {
  emit('preview-media', media)
}

function openMediaInWindow(media) {
  if (!media?.id) return
  window.open(`${apiStore.baseUrl}/media/${media.id}/file?token=${userStore.token}`, '_blank')
}

async function deleteMedia(media) {
  if (!media?.id) return
  
  // Show confirmation dialog
  const confirmed = confirm(`Are you sure you want to delete "${media.filename || media.label}"? This action cannot be undone.`)
  if (!confirmed) return
  
  console.log('Deleting media:', media.filename || media.label)
  
  try {
    const result = await mediaStore.delete(media.id)
    
    if (result.success) {
      console.log('Media deleted successfully')
      // Media is automatically removed from the store, so the UI will update
    } else {
      console.error('Failed to delete media:', result.error)
      alert(`Failed to delete media: ${result.error}`)
    }
  } catch (error) {
    console.error('Error deleting media:', error)
    alert('Failed to delete media. Please try again.')
  }
}
</script>