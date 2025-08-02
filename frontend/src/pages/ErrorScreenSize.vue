<template>
  <div class="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8 text-center">
      <!-- Icon -->
      <div class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
        </svg>
      </div>

      <!-- Title -->
      <h1 class="text-2xl font-bold text-gray-900 mb-4">
        Screen Too Small
      </h1>

      <!-- Description -->
      <div class="text-gray-600 mb-6 space-y-3">
        <p>
          WriteDarker requires minimum screen dimensions for the best writing experience.
        </p>
        <div class="bg-gray-50 rounded-lg p-4 space-y-3">
          <!-- Width Requirements -->
          <div class="flex justify-between items-center">
            <div class="flex items-center">
              <svg v-if="widthValid" class="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              <svg v-else class="w-4 h-4 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              <span class="text-sm font-medium text-gray-700">Width:</span>
            </div>
            <div class="text-sm font-mono">
              <span :class="widthValid ? 'text-green-600' : 'text-red-600'">{{ currentWidth }}px</span>
              <span class="text-gray-500 mx-1">/</span>
              <span class="text-gray-600">{{ minWidth }}px</span>
            </div>
          </div>
          
          <!-- Height Requirements -->
          <div class="flex justify-between items-center">
            <div class="flex items-center">
              <svg v-if="heightValid" class="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              <svg v-else class="w-4 h-4 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              <span class="text-sm font-medium text-gray-700">Height:</span>
            </div>
            <div class="text-sm font-mono">
              <span :class="heightValid ? 'text-green-600' : 'text-red-600'">{{ currentHeight }}px</span>
              <span class="text-gray-500 mx-1">/</span>
              <span class="text-gray-600">{{ minHeight }}px</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress Bars -->
      <div class="mb-6 space-y-3">
        <!-- Width Progress -->
        <div>
          <div class="flex justify-between text-xs text-gray-500 mb-1">
            <span>Width Progress</span>
            <span>{{ Math.round((currentWidth / minWidth) * 100) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="widthValid ? 'bg-green-500' : 'bg-red-500'"
              :style="{ width: Math.min(100, (currentWidth / minWidth) * 100) + '%' }"
            ></div>
          </div>
        </div>
        
        <!-- Height Progress -->
        <div>
          <div class="flex justify-between text-xs text-gray-500 mb-1">
            <span>Height Progress</span>
            <span>{{ Math.round((currentHeight / minHeight) * 100) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="heightValid ? 'bg-green-500' : 'bg-red-500'"
              :style="{ width: Math.min(100, (currentHeight / minHeight) * 100) + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Instructions -->
      <div class="text-sm text-gray-600 mb-6">
        <p class="mb-2">To continue, ensure both width and height requirements are met:</p>
        <ul class="text-left space-y-1">
          <li class="flex items-center">
            <svg class="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            Resize your browser window (width & height)
          </li>
          <li class="flex items-center">
            <svg class="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            Use a larger screen or device
          </li>
          <li class="flex items-center">
            <svg class="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            Zoom out in your browser
          </li>
          <li class="flex items-center">
            <svg class="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            Maximize your browser window
          </li>
        </ul>
      </div>

      <!-- Retry Button -->
      <button
        @click="checkScreenSize"
        class="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium py-3 px-4 rounded-xl hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200"
      >
        <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        Check Again
      </button>

      <!-- Footer -->
      <div class="mt-6 pt-4 border-t border-gray-100">
        <p class="text-xs text-gray-500">
          WriteDarker works best on desktop and tablet devices
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { AppConfig } from '../config/app'

const router = useRouter()

// Get minimum dimensions from application config
const minWidth = AppConfig.MIN_WIDTH
const minHeight = AppConfig.MIN_HEIGHT
const currentWidth = ref(window.innerWidth)
const currentHeight = ref(window.innerHeight)

// Computed properties for validation
const widthValid = computed(() => currentWidth.value >= minWidth)
const heightValid = computed(() => currentHeight.value >= minHeight)
const allValid = computed(() => widthValid.value && heightValid.value)

function updateScreenSize() {
  currentWidth.value = window.innerWidth
  currentHeight.value = window.innerHeight
}

function checkScreenSize() {
  updateScreenSize()
  if (allValid.value) {
    // Redirect back to the previous page or dashboard
    const from = router.options.history.state.back
    if (from && from !== '/error-screen-size') {
      router.push(from)
    } else {
      router.push('/dashboard')
    }
  }
}

onMounted(() => {
  window.addEventListener('resize', updateScreenSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenSize)
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>