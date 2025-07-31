<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="handleBackdropClick">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4" @click.stop>
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Edit Media</h3>
        <button @click="handleClose" class="text-gray-400 hover:text-gray-600 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="p-6 space-y-4 max-h-[60vh] overflow-auto">
        <div v-if="error" class="p-3 bg-red-50 border border-red-200 text-red-800 rounded">
          {{ error }}
        </div>
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
          ></textarea>
        </div>
      </div>

      <div class="flex items-center justify-end p-6 border-t border-gray-200 space-x-3">
        <BaseButton variant="outline" @click="handleClose">Cancel</BaseButton>
        <BaseButton variant="primary" :loading="loading" @click="handleSubmit">Save Changes</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useMediaStore } from '../../stores/media'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  show: { type: Boolean, default: false },
  media: { type: Object, default: null }
})

const emit = defineEmits(['close', 'updated'])

const mediaStore = useMediaStore()
const loading = ref(false)
const error = ref('')
const formData = ref({ label: '', description: '' })

watch(() => props.media, (m) => {
  if (m) {
    formData.value = {
      label: m.label || '',
      description: m.description || ''
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
  if (!props.media) return
  loading.value = true
  error.value = ''
  const { success, data, error: err } = await mediaStore.update(props.media.id, formData.value)
  if (success) {
    emit('updated', data)
    handleClose()
  } else {
    error.value = err || 'Failed to update media'
  }
  loading.value = false
}
</script>

<style scoped>
.resize-vertical {
  resize: vertical;
}
</style>
