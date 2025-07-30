<template>
  <div v-if="isInitializing" class="min-h-screen bg-gradient-to-br from-orange-50 via-white to-orange-100 flex items-center justify-center">
    <div class="text-center">
      <div class="w-16 h-16 bg-gradient-to-r from-orange-400 to-orange-600 rounded-full mx-auto mb-4 flex items-center justify-center animate-pulse">
        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.828 2.828 0 114 4L9 19.5l-4.5-1L9 14.5z"></path>
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">WriteDarker</h2>
      <p class="text-gray-600">Initializing...</p>
    </div>
  </div>
  <router-view v-else />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from './stores/user'

const userStore = useUserStore()
const isInitializing = ref(true)

onMounted(async () => {
  try {
    // Initialize authentication if token exists
    await userStore.initializeAuth()
  } catch (error) {
    // Ignore auth errors on startup
    console.warn('Auth initialization failed:', error)
  } finally {
    // Always stop loading after initialization attempt
    isInitializing.value = false
  }
})
</script>
