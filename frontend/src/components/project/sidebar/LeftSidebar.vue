<template>
  <div 
    :class="[
      'bg-white border-r border-gray-200 flex flex-col transition-all duration-300',
      props.collapsed ? 'w-12' : 'w-80 sm:w-72 lg:w-80'
    ]"
  >
    <!-- Sidebar header -->
    <div class="p-3 border-b border-gray-200 flex items-center justify-between">
      <div v-if="!props.collapsed" class="text-xs font-medium text-gray-600 uppercase tracking-wide">References & Files</div>
      <button
        @click="$emit('toggle-collapse')"
        class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="props.collapsed ? 'M9 5l7 7-7 7' : 'M15 19l-7-7 7-7'"></path>
        </svg>
      </button>
    </div>

    <!-- Sidebar content -->
    <div v-if="!props.collapsed" class="column flex-1 overflow-y-auto min-h-0 sidebar-scrollable">
      <!-- Add Files Button -->
      <div class="col-auto q-pa-sm">
        <q-btn
          :disable="!props.projectId || props.isNewProject"
          @click="handleAddFilesClick"
          outline
          color="orange-6"
          size="sm"
          class="full-width q-py-sm"
          icon="add"
        >
          <span class="q-ml-xs">{{ (!props.projectId || props.isNewProject) ? 'Save project first' : 'Add Files' }}</span>
        </q-btn>
      </div>

      <!-- References and Media Files List -->
      <div class="col">
        <q-list dense class="q-pa-none">
          <ReferenceList
            v-model:expanded="referencesExpanded"
            :references="props.references"
            @add="handleAddReference"
            @select="openReference"
            @preview="previewReference"
            @open-in-window="openReferenceInWindow"
          />
          <MediaList
            v-model:expanded="mediaFilesExpanded"
            :media="props.mediaFiles"
            @select="editMedia"
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

    <!-- Dialogs -->
    <MediaPreviewDialog
      :show="showMediaPreview"
      :media="selectedPreviewMedia"
      @close="showMediaPreview = false"
    />

    <MediaEditDialog
      :show="showMediaEdit"
      :media="selectedMedia"
      @close="showMediaEdit = false"
      @updated="handleMediaUpdated"
    />

    <ReferencePreviewDialog
      :show="showReferencePreview"
      :reference="selectedReference"
      @close="showReferencePreview = false"
    />

    <ReferenceSearchDialog
      v-if="props.projectId"
      :show="showReferenceSearch"
      :project-id="props.projectId"
      @close="showReferenceSearch = false"
      @added="handleReferenceAdded"
    />

    <FileActionDialog
      :show="showFileAction"
      @close="showFileAction = false"
      @upload-pdf="handleUploadPdf"
      @search-pubmed="handleSearchPubMed"
      @upload-media="handleUploadMedia"
    />

    <FileUpload
      :show="showPdfUpload"
      accept=".pdf"
      @close="showPdfUpload = false"
      @files-selected="uploadPdfFiles"
    />

    <FileUpload
      :show="showMediaUpload"
      accept="image/*,audio/*,video/*"
      @close="showMediaUpload = false"
      @files-selected="uploadMediaFiles"
    />

    <PubMedSearch
      :show="showPubMedSearch"
      @close="showPubMedSearch = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ReferenceList from '../ReferenceList.vue'
import MediaList from '../MediaList.vue'
import MediaPreviewDialog from '../../ui/MediaPreviewDialog.vue'
import MediaEditDialog from '../../ui/MediaEditDialog.vue'
import ReferencePreviewDialog from '../../ui/ReferencePreviewDialog.vue'
import ReferenceSearchDialog from '../ReferenceSearchDialog.vue'
import FileActionDialog from '../FileActionDialog.vue'
import FileUpload from '../../ui/FileUpload.vue'
import PubMedSearch from '../../ui/PubMedSearch.vue'
import { useApiStore } from '../../../stores/api'
import { useUserStore } from '../../../stores/user'
import { useMediaStore } from '../../../stores/media'
import { useReferenceStore } from '../../../stores/reference'

// Props
const props = defineProps({
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
  'media-updated',
  'reference-added'
])

// Stores
const apiStore = useApiStore()
const userStore = useUserStore()
const mediaStore = useMediaStore()
const referenceStore = useReferenceStore()

// Local state
const referencesExpanded = ref(true)
const mediaFilesExpanded = ref(true)

// Dialog states
const showFileAction = ref(false)
const showPdfUpload = ref(false)
const showMediaUpload = ref(false)
const showPubMedSearch = ref(false)
const showReferenceSearch = ref(false)
const showMediaEdit = ref(false)
const showReferencePreview = ref(false)
const showMediaPreview = ref(false)
const selectedMedia = ref(null)
const selectedReference = ref(null)
const selectedPreviewMedia = ref(null)
const droppedFiles = ref([])

// Methods
function handleAddFilesClick() {
  showFileAction.value = true
}

function openReference(ref) {
  if (!ref?.id) return
  window.open(`${apiStore.baseUrl}/references/${ref.id}/file?token=${userStore.token}`, '_blank')
}

function previewReference(reference) {
  if (!reference) return
  selectedReference.value = reference
  showReferencePreview.value = true
}

function openReferenceInWindow(reference) {
  if (!reference?.id) return
  window.open(`${apiStore.baseUrl}/references/${reference.id}/file?token=${userStore.token}`, '_blank')
}

function previewMedia(media) {
  if (!media) return
  selectedPreviewMedia.value = media
  showMediaPreview.value = true
}

function openMediaInWindow(media) {
  if (!media?.id) return
  window.open(`${apiStore.baseUrl}/media/${media.id}/file?token=${userStore.token}`, '_blank')
}

function editMedia(media) {
  if (!media) return
  selectedMedia.value = media
  showMediaEdit.value = true
}

function handleAddReference() {
  showReferenceSearch.value = true
}

// File handling methods
async function handleUploadPdf() {
  if (droppedFiles.value.length) {
    await uploadPdfFiles(droppedFiles.value)
    droppedFiles.value = []
    showFileAction.value = false
  } else {
    showFileAction.value = false
    showPdfUpload.value = true
  }
}

async function uploadPdfFiles(files) {
  for (const file of files) {
    await referenceStore.upload({
      projectIds: props.projectId ? [props.projectId] : [],
      query: file.name,
      file
    })
  }
}

function handleSearchPubMed() {
  showFileAction.value = false
  showPubMedSearch.value = true
}

async function handleUploadMedia() {
  if (droppedFiles.value.length) {
    await uploadMediaFiles(droppedFiles.value)
    droppedFiles.value = []
    showFileAction.value = false
  } else {
    showFileAction.value = false
    showMediaUpload.value = true
  }
}

async function uploadMediaFiles(files) {
  if (!props.projectId) {
    if (props.isNewProject) {
      console.error('Cannot upload media files to a new project. Please save the project first.')
      alert('Please save your project before uploading media files.')
      return
    } else {
      console.error('No project ID available for media upload')
      return
    }
  }
  
  console.log('Starting media upload for', files.length, 'files')
  
  let successCount = 0
  let errorCount = 0
  
  for (const file of files) {
    console.log('Uploading file:', file.name, 'Type:', file.type, 'Size:', file.size)
    try {
      const result = await mediaStore.upload({ 
        projectId: props.projectId, 
        file, 
        label: file.name 
      })
      
      if (result.success) {
        console.log('Upload successful for:', file.name)
        successCount++
      } else {
        console.error('Upload failed for:', file.name, 'Error:', result.error)
        errorCount++
      }
    } catch (error) {
      console.error('Upload error for:', file.name, error)
      errorCount++
    }
  }
  
  // Show summary
  console.log(`Upload complete: ${successCount} successful, ${errorCount} failed`)
  
  // Refresh the media list after upload
  if (props.projectId && successCount > 0) {
    try {
      await mediaStore.fetch(props.projectId)
      console.log('Media list refreshed')
    } catch (error) {
      console.error('Failed to refresh media list:', error)
    }
  }
}

async function handleMediaUpdated() {
  if (props.projectId) {
    await mediaStore.fetch(props.projectId)
  }
  emit('media-updated')
}

async function handleReferenceAdded() {
  if (props.projectId) {
    await referenceStore.fetchAll(props.projectId)
  }
  emit('reference-added')
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