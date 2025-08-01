<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="handleBackdropClick">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4" @click.stop>
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Media Preview & Edit</h3>
        <button @click="handleClose" class="text-gray-400 hover:text-gray-600 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="p-6 space-y-6 max-h-[70vh] overflow-auto">
        <div v-if="error" class="p-3 bg-red-50 border border-red-200 text-red-800 rounded">
          {{ error }}
        </div>
        
        <!-- Image Preview Section -->
        <div v-if="media && isImageFile" class="text-center">
          <h4 class="text-sm font-medium text-gray-700 mb-3">Preview</h4>
          <div class="bg-gray-50 rounded-lg p-4 inline-block">
            <img 
              :src="imageUrl" 
              :alt="media.filename || media.label"
              class="max-w-full max-h-64 object-contain rounded shadow-sm"
              @error="handleImageError"
            />
          </div>
        </div>

        <!-- File Info Section -->
        <div v-if="media" class="bg-gray-50 rounded-lg p-4">
          <h4 class="text-sm font-medium text-gray-700 mb-2">File Information</h4>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-600">Filename:</span>
              <span class="ml-2 font-medium">{{ media.filename || 'Unknown' }}</span>
            </div>
            <div>
              <span class="text-gray-600">Type:</span>
              <span class="ml-2 font-medium">{{ media.filetype || 'Unknown' }}</span>
            </div>
            <div>
              <span class="text-gray-600">Size:</span>
              <span class="ml-2 font-medium">{{ formatFileSize(media.filesize) }}</span>
            </div>
          </div>
        </div>

        <!-- Edit Metadata Section -->
        <div v-if="showEditForm">
          <h4 class="text-sm font-medium text-gray-700 mb-3">Edit Metadata</h4>
          <div class="space-y-4">
            <div>
              <label for="label" class="block text-sm font-medium text-gray-700 mb-1">Label</label>
              <input
                id="label"
                v-model="formData.label"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                id="description"
                v-model="formData.description"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
                rows="3"
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between p-6 border-t border-gray-200">
        <div class="space-x-3">
          <BaseButton 
            v-if="!showEditForm" 
            variant="outline" 
            @click="showEditForm = true"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit Metadata
          </BaseButton>
        </div>
        <div class="flex items-center space-x-3">
          <BaseButton variant="outline" @click="handleClose">
            {{ showEditForm ? 'Cancel' : 'Close' }}
          </BaseButton>
          <BaseButton 
            v-if="showEditForm" 
            variant="primary" 
            :loading="loading" 
            @click="handleSubmit"
          >
            Save Changes
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useMediaStore } from '../../stores/media'
import { useUserStore } from '../../stores/user'
import { useApiStore } from '../../stores/api'
import BaseButton from './BaseButton.vue'

const apiStore = useApiStore()

const props = defineProps({
  show: { type: Boolean, default: false },
  media: { type: Object, default: null }
})

const emit = defineEmits(['close', 'updated'])

const mediaStore = useMediaStore()
const userStore = useUserStore()
const loading = ref(false)
const error = ref('')
const showEditForm = ref(false)
const formData = ref({ label: '', description: '' })

// Check if the media is an image file
const isImageFile = computed(() => {
  if (!props.media?.filetype) return false
  return props.media.filetype.startsWith('image/')
})

// Generate image URL for preview
const imageUrl = computed(() => {
  if (!props.media?.id || !isImageFile.value) return ''
  return `${apiStore.baseUrl}/documents/${props.media.id}/file?token=${userStore.token}`
})

watch(() => props.media, (m) => {
  if (m) {
    formData.value = {
      label: m.label || '',
      description: m.description || ''
    }
  }
  // Reset edit form when media changes
  showEditForm.value = false
  error.value = ''
}, { immediate: true })

watch(() => props.show, (show) => {
  if (!show) {
    showEditForm.value = false
    error.value = ''
  }
})

function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  if (!bytes) return 'Unknown'
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

function handleImageError() {
  error.value = 'Failed to load image preview'
}

function handleClose() {
  error.value = ''
  showEditForm.value = false
  emit('close')
}

function handleBackdropClick() {
  if (!showEditForm.value) {
    emit('close')
  }
}

async function handleSubmit() {
  if (!props.media) return
  loading.value = true
  error.value = ''
  
  try {
    const { success, data, error: err } = await mediaStore.update(props.media.id, formData.value)
    if (success) {
      emit('updated', data)
      showEditForm.value = false
    } else {
      error.value = err || 'Failed to update media'
    }
  } catch (err) {
    error.value = 'Failed to update media'
    console.error('Media update error:', err)
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
