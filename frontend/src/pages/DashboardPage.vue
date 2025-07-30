<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo and title -->
          <div class="flex items-center">
            <div class="w-8 h-8 bg-gradient-to-r from-orange-400 to-orange-600 rounded-lg flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.828 2.828 0 114 4L9 19.5l-4.5-1L9 14.5z"></path>
              </svg>
            </div>
            <h1 class="text-xl font-semibold text-gray-900">WriteDarker Dashboard</h1>
          </div>

          <!-- User menu -->
          <div class="flex items-center space-x-4">
            <div class="text-sm text-gray-700">
              Welcome back, <span class="font-medium">{{ userStore.userDisplayName }}</span>
            </div>
            
            <div class="relative" ref="userMenuRef">
              <button
                @click="showUserMenu = !showUserMenu"
                class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {{ userStore.userInitials }}
                </div>
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>

              <!-- User dropdown -->
              <Transition
                name="dropdown"
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div
                  v-if="showUserMenu"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50"
                >
                  <button
                    @click="handleLogout"
                    class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  >
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                    </svg>
                    Sign out
                  </button>
                </div>
              </Transition>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome section -->
      <div class="mb-8">
        <BaseCard variant="elevated" padding="lg">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-orange-400 to-orange-600 rounded-full mx-auto mb-4 flex items-center justify-center">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Welcome to WriteDarker!</h2>
            <p class="text-gray-600 mb-6">You're successfully logged in and ready to start writing.</p>
            
            <div class="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-6">
              <div class="flex items-start">
                <svg class="w-5 h-5 text-orange-400 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div class="text-sm text-orange-700">
                  <p class="font-medium mb-1">Protected Route Demo</p>
                  <p>This dashboard page is protected by authentication. You can only access it when logged in!</p>
                </div>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- User info section -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <BaseCard variant="bordered" padding="md">
          <template #header>
            <div class="flex items-center">
              <svg class="w-5 h-5 text-orange-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              <h3 class="text-lg font-semibold text-gray-900">Profile</h3>
            </div>
          </template>
          
          <div class="space-y-3">
            <div>
              <label class="text-sm font-medium text-gray-500">Username</label>
              <p class="text-gray-900">{{ userStore.currentUser?.username }}</p>
            </div>
            <div v-if="userStore.currentUser?.email">
              <label class="text-sm font-medium text-gray-500">Email</label>
              <p class="text-gray-900">{{ userStore.currentUser.email }}</p>
            </div>
            <div v-if="userStore.currentUser?.age">
              <label class="text-sm font-medium text-gray-500">Age</label>
              <p class="text-gray-900">{{ userStore.currentUser.age }}</p>
            </div>
          </div>
        </BaseCard>

        <BaseCard variant="bordered" padding="md">
          <template #header>
            <div class="flex items-center">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <h3 class="text-lg font-semibold text-gray-900">Status</h3>
            </div>
          </template>
          
          <div class="space-y-3">
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
              <span class="text-sm text-gray-600">Authenticated</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
              <span class="text-sm text-gray-600">Session Active</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-orange-400 rounded-full mr-2"></div>
              <span class="text-sm text-gray-600">Ready to Write</span>
            </div>
          </div>
        </BaseCard>

        <BaseCard variant="bordered" padding="md">
          <template #header>
            <div class="flex items-center">
              <svg class="w-5 h-5 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              <h3 class="text-lg font-semibold text-gray-900">Quick Actions</h3>
            </div>
          </template>
          
          <div class="space-y-3">
            <BaseButton variant="outline" size="sm" full-width>
              New Document
            </BaseButton>
            <BaseButton variant="outline" size="sm" full-width>
              View Projects
            </BaseButton>
            <BaseButton variant="outline" size="sm" full-width>
              Settings
            </BaseButton>
          </div>
        </BaseCard>
      </div>

      <!-- Features preview -->
      <BaseCard variant="elevated" padding="lg">
        <template #header>
          <h3 class="text-xl font-semibold text-gray-900">Coming Soon</h3>
          <p class="text-gray-600 mt-1">Features that will be available in WriteDarker</p>
        </template>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="text-center p-4 bg-orange-50 rounded-lg">
            <svg class="w-8 h-8 text-orange-500 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <h4 class="font-medium text-gray-900 mb-2">Document Editor</h4>
            <p class="text-sm text-gray-600">Rich text editor with AI assistance</p>
          </div>
          
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <svg class="w-8 h-8 text-blue-500 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
            </svg>
            <h4 class="font-medium text-gray-900 mb-2">Project Management</h4>
            <p class="text-sm text-gray-600">Organize your writing projects</p>
          </div>
          
          <div class="text-center p-4 bg-green-50 rounded-lg">
            <svg class="w-8 h-8 text-green-500 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            <h4 class="font-medium text-gray-900 mb-2">AI Assistance</h4>
            <p class="text-sm text-gray-600">Smart writing suggestions and help</p>
          </div>
        </div>
      </BaseCard>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import BaseCard from '../components/ui/BaseCard.vue'
import BaseButton from '../components/ui/BaseButton.vue'

const router = useRouter()
const userStore = useUserStore()

const showUserMenu = ref(false)
const userMenuRef = ref(null)

// Handle logout
const handleLogout = async () => {
  try {
    await userStore.logout()
    router.push('/auth')
  } catch (error) {
    console.error('Logout error:', error)
    // Force redirect even if logout fails
    router.push('/auth')
  }
}

// Close user menu when clicking outside
const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>