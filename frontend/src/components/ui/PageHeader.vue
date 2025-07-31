<template>
  <header class="bg-white/90 backdrop-blur-sm shadow-sm border-b border-gray-200 flex-shrink-0">
    <div class="px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-14 min-h-[3.5rem]">
        <!-- Left side - Back button and title -->
        <div class="flex items-center space-x-4">
          <button
            v-if="showBackButton"
            @click="goBack"
            class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          
          <div class="flex items-center">
            <div v-if="icon" class="w-6 h-6 bg-gradient-to-r from-orange-400 to-orange-600 rounded-md flex items-center justify-center mr-2">
              <component :is="icon" class="w-3 h-3 text-white" />
            </div>
            <h1 class="text-sm font-medium text-gray-900">{{ title }}</h1>
          </div>
        </div>

        <!-- Right side - Actions -->
        <div class="flex items-center space-x-2 sm:space-x-3">
          <slot name="actions">
            <!-- Default actions slot -->
          </slot>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  showBackButton: {
    type: Boolean,
    default: false
  },
  backRoute: {
    type: String,
    default: '/dashboard'
  },
  icon: {
    type: String,
    default: null
  }
})

const goBack = () => {
  router.push(props.backRoute)
}
</script> 