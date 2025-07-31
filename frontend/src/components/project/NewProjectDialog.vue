<template>
  <BaseModal 
    :show="show" 
    @close="handleClose"
    title="Create New Project"
    subtitle="Enter the details for your new project"
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
      <BaseButton 
        @click="handleClose"
        variant="outline" 
        size="sm"
        :disabled="loading"
      >
        Cancel
      </BaseButton>
      <BaseButton 
        @click="handleSubmit"
        variant="primary" 
        size="sm"
        :disabled="loading || !formData.label.trim()"
        :loading="loading"
      >
        {{ loading ? 'Creating...' : 'Create Project' }}
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import BaseModal from '../ui/BaseModal.vue'
import BaseButton from '../ui/BaseButton.vue'
import { useProjectStore } from '../../stores/project'

const props = defineProps({
  show: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'created'])

const projectStore = useProjectStore()
const loading = ref(false)
const error = ref('')

const formData = reactive({
  label: '',
  description: '',
  coauthors: ''
})

// Reset form when dialog opens
watch(() => props.show, (newVal) => {
  if (newVal) {
    formData.label = ''
    formData.description = ''
    formData.coauthors = ''
    error.value = ''
  }
})

function handleClose() {
  if (!loading.value) {
    emit('close')
  }
}

async function handleSubmit() {
  if (!formData.label.trim()) {
    error.value = 'Project name is required'
    return
  }

  loading.value = true
  error.value = ''

  try {
    console.log('Creating project with data:', {
      label: formData.label.trim(),
      description: formData.description.trim(),
      coauthors: formData.coauthors.trim()
    })
    
    const result = await projectStore.create({
      label: formData.label.trim(),
      description: formData.description.trim(),
      coauthors: formData.coauthors.trim()
    })

    console.log('Project creation result:', result)

    if (result && result.success) {
      console.log('Project created successfully:', result.data)
      emit('created', result.data)
      handleClose()
    } else {
      console.error('Project creation failed:', result)
      error.value = result?.error || 'Failed to create project'
    }
  } catch (err) {
    console.error('Error creating project:', err)
    error.value = 'An unexpected error occurred'
  } finally {
    loading.value = false
  }
}
</script>