<template>
  <BaseModal 
    :show="show" 
    @close="handleClose"
    title="Edit Project"
    subtitle="Update your project information"
    size="md"
    :close-on-backdrop="false"
  >
    <div class="space-y-4">
      <!-- Project Name -->
      <div>
        <label for="project-name" class="block text-sm font-medium text-gray-700 mb-2">
          Project Name *
        </label>
        <input
          id="project-name"
          v-model="formData.label"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          placeholder="Enter project name..."
          :disabled="loading"
          @keyup.enter="handleSubmit"
        />
      </div>

      <!-- Project Description -->
      <div>
        <label for="project-description" class="block text-sm font-medium text-gray-700 mb-2">
          Description
        </label>
        <textarea
          id="project-description"
          v-model="formData.description"
          rows="3"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-vertical"
          placeholder="Brief description of your project..."
          :disabled="loading"
        ></textarea>
      </div>

      <!-- Co-authors -->
      <div>
        <label for="project-coauthors" class="block text-sm font-medium text-gray-700 mb-2">
          Co-authors
        </label>
        <input
          id="project-coauthors"
          v-model="formData.coauthors"
          type="text"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          placeholder="Names of co-authors (optional)..."
          :disabled="loading"
          @keyup.enter="handleSubmit"
        />
      </div>

      <!-- Error message -->
      <div v-if="error" class="p-3 rounded-lg bg-red-50 border border-red-200">
        <p class="text-sm text-red-700">{{ error }}</p>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-between items-center w-full">
        <BaseButton 
          @click="showDeleteConfirm"
          variant="danger" 
          size="sm"
          :disabled="loading"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1-1H8a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
          Delete Project
        </BaseButton>
        <BaseButton 
          v-if="hasChanges"
          @click="handleSubmit"
          variant="primary" 
          size="sm"
          :disabled="loading || !formData.label.trim()"
          :loading="loading"
        >
          {{ loading ? 'Updating...' : 'Update Project' }}
        </BaseButton>
      </div>
    </template>

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      :show="showDeleteDialog"
      type="danger"
      title="Delete Project"
      subtitle="This action cannot be undone"
      :message="`Are you sure you want to delete '${project?.label}'? This will permanently remove the project and all associated data.`"
      details="All references, media files, and documents associated with this project will be deleted."
      confirm-text="Delete Project"
      cancel-text="Cancel"
      :loading="deleting"
      loading-text="Deleting..."
      confirm-variant="danger"
      @confirm="handleDelete"
      @cancel="hideDeleteConfirm"
    />
  </BaseModal>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import BaseModal from '../ui/BaseModal.vue'
import BaseButton from '../ui/BaseButton.vue'
import ConfirmDialog from '../ui/ConfirmDialog.vue'
import { useProjectStore } from '../../stores/project'

const props = defineProps({
  show: { type: Boolean, default: false },
  project: { type: Object, default: null }
})

const emit = defineEmits(['close', 'updated', 'deleted'])

const projectStore = useProjectStore()
const loading = ref(false)
const deleting = ref(false)
const error = ref('')
const showDeleteDialog = ref(false)

const formData = reactive({
  label: '',
  description: '',
  coauthors: ''
})

const originalData = ref({
  label: '',
  description: '',
  coauthors: ''
})

// Check if form has changes
const hasChanges = computed(() => {
  return (
    formData.label.trim() !== originalData.value.label.trim() ||
    formData.description.trim() !== originalData.value.description.trim() ||
    formData.coauthors.trim() !== originalData.value.coauthors.trim()
  )
})

// Reset form when dialog opens or project changes
watch(() => [props.show, props.project], ([newShow, newProject]) => {
  if (newShow && newProject) {
    const label = newProject.label || ''
    const description = newProject.description || ''
    const coauthors = newProject.coauthors || ''
    
    formData.label = label
    formData.description = description
    formData.coauthors = coauthors
    
    originalData.value = {
      label,
      description,
      coauthors
    }
    
    error.value = ''
  }
})

function handleClose() {
  if (!loading.value && !deleting.value) {
    emit('close')
  }
}

function showDeleteConfirm() {
  showDeleteDialog.value = true
}

function hideDeleteConfirm() {
  showDeleteDialog.value = false
}

async function handleSubmit() {
  if (!formData.label.trim() || !props.project) {
    return
  }

  loading.value = true
  error.value = ''

  try {
    const result = await projectStore.update(props.project.id, {
      label: formData.label.trim(),
      description: formData.description.trim(),
      coauthors: formData.coauthors.trim()
    })

    if (result && result.success) {
      emit('updated', result.data)
      handleClose()
    } else {
      error.value = result?.error || 'Failed to update project'
    }
  } catch (err) {
    console.error('Error updating project:', err)
    error.value = 'An unexpected error occurred'
  } finally {
    loading.value = false
  }
}

async function handleDelete() {
  if (!props.project) return

  deleting.value = true
  
  try {
    const result = await projectStore.delete(props.project.id)
    
    if (result && result.success) {
      emit('deleted', props.project)
      showDeleteDialog.value = false
      handleClose()
    } else {
      error.value = result?.error || 'Failed to delete project'
      showDeleteDialog.value = false
    }
  } catch (err) {
    console.error('Error deleting project:', err)
    error.value = 'An unexpected error occurred'
    showDeleteDialog.value = false
  } finally {
    deleting.value = false
  }
}
</script>