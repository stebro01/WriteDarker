<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="handleBackdropClick">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4" @click.stop>
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div class="flex items-center">
          <div class="w-10 h-10 rounded-full flex items-center justify-center mr-3" :class="iconClass">
            <component :is="icon" class="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900">{{ title }}</h3>
            <p class="text-sm text-gray-600">{{ subtitle }}</p>
          </div>
        </div>
        <button @click="handleCancel" class="text-gray-400 hover:text-gray-600 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6">
        <p class="text-gray-700 mb-6">{{ message }}</p>
        
        <!-- Additional details if provided -->
        <div v-if="details" class="bg-gray-50 rounded-lg p-4 mb-6">
          <div class="text-sm text-gray-600">{{ details }}</div>
        </div>

        <!-- Custom content slot -->
        <slot name="content"></slot>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-end space-x-3 p-6 border-t border-gray-200">
        <BaseButton 
          @click="handleCancel"
          variant="outline" 
          size="sm"
          :disabled="loading"
        >
          {{ cancelText }}
        </BaseButton>
        <BaseButton 
          @click="handleConfirm"
          :variant="confirmVariant" 
          size="sm"
          :disabled="loading"
        >
          <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          {{ loading ? loadingText : confirmText }}
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  subtitle: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    required: true
  },
  details: {
    type: String,
    default: ''
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  loadingText: {
    type: String,
    default: 'Processing...'
  },
  loading: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'warning', // 'warning', 'danger', 'info', 'success'
    validator: (value) => ['warning', 'danger', 'info', 'success'].includes(value)
  },
  confirmVariant: {
    type: String,
    default: 'primary'
  }
})

const emit = defineEmits(['confirm', 'cancel', 'close'])

// Icon and styling based on type
const icon = computed(() => {
  switch (props.type) {
    case 'danger':
      return 'ExclamationTriangleIcon'
    case 'warning':
      return 'ExclamationTriangleIcon'
    case 'info':
      return 'InformationCircleIcon'
    case 'success':
      return 'CheckCircleIcon'
    default:
      return 'ExclamationTriangleIcon'
  }
})

const iconClass = computed(() => {
  switch (props.type) {
    case 'danger':
      return 'bg-red-500'
    case 'warning':
      return 'bg-yellow-500'
    case 'info':
      return 'bg-blue-500'
    case 'success':
      return 'bg-green-500'
    default:
      return 'bg-yellow-500'
  }
})

// Event handlers
const handleConfirm = () => {
  if (!props.loading) {
    emit('confirm')
  }
}

const handleCancel = () => {
  if (!props.loading) {
    emit('cancel')
    emit('close')
  }
}

const handleBackdropClick = () => {
  if (!props.loading) {
    emit('close')
  }
}
</script> 