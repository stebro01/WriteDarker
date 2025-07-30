<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-orange-50/20">
    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-sm shadow-sm border-b border-orange-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-14">
          <!-- Logo and title -->
          <div class="flex items-center">
            <div class="w-7 h-7 bg-gradient-to-r from-orange-400 to-orange-600 rounded-lg flex items-center justify-center mr-3">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.828 2.828 0 114 4L9 19.5l-4.5-1L9 14.5z"></path>
              </svg>
            </div>
            <h1 class="text-base font-medium text-gray-800">WriteDarker</h1>
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
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Welcome section -->
      <div class="mb-6">
        <div class="text-center mb-8">
          <h2 class="text-lg font-medium text-gray-900 mb-2">Welcome back, {{ userStore.userDisplayName }}!</h2>
          <p class="text-gray-600">Ready to continue your writing journey?</p>
        </div>
      </div>

      <!-- Main dashboard cards -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- User Profile Card -->
        <BaseCard variant="glass" padding="lg" class="hover:shadow-xl transition-all duration-300 group">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <div class="text-2xl font-bold text-white">{{ userStore.userInitials }}</div>
            </div>
            <div class="text-base font-medium text-gray-900 mb-2">{{ userStore.userDisplayName }}</div>
            <p class="text-sm text-gray-600 mb-4">@{{ userStore.currentUser?.username }}</p>
            
            <div class="space-y-2 text-left bg-orange-50/50 rounded-lg p-3">
              <div v-if="userStore.currentUser?.email" class="flex items-center text-sm">
                <svg class="w-4 h-4 text-orange-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
                <span class="text-gray-700">{{ userStore.currentUser.email }}</span>
              </div>
              <div class="flex items-center text-sm">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-gray-700">Active Writer</span>
              </div>
            </div>
          </div>
        </BaseCard>

        <!-- Projects Card -->
        <BaseCard variant="glass" padding="lg" class="hover:shadow-xl transition-all duration-300 group">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
              </svg>
            </div>
            <div class="text-base font-medium text-gray-900 mb-2">Projects</div>
            <p class="text-sm text-gray-600 mb-4">Manage your writing projects</p>
            
            <div class="space-y-3">
              <div class="bg-blue-50/50 rounded-lg p-3">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-700">Active Projects</span>
                  <span class="text-base font-semibold text-blue-600">3</span>
                </div>
                <div class="text-xs text-gray-500">2 in progress, 1 completed</div>
              </div>
              
              <div class="space-y-2">
                <BaseButton 
                  @click="navigateToProject('new')"
                  variant="primary" 
                  size="sm" 
                  full-width
                  class="group-hover:shadow-md transition-shadow"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                  New Project
                </BaseButton>
                <BaseButton 
                  @click="navigateToProject('existing')"
                  variant="outline" 
                  size="sm" 
                  full-width
                >
                  View All Projects
                </BaseButton>
              </div>
            </div>
          </div>
        </BaseCard>

        <!-- References Card -->
        <BaseCard variant="glass" padding="lg" class="hover:shadow-xl transition-all duration-300 group">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
            <div class="text-base font-medium text-gray-900 mb-2">References</div>
            <p class="text-sm text-gray-600 mb-4">Research materials & sources</p>
            
            <div class="space-y-3">
              <div class="bg-green-50/50 rounded-lg p-3">
                <div class="grid grid-cols-2 gap-3 text-center">
                  <div>
                    <div class="text-base font-semibold text-green-600">{{ pdfCount }}</div>
                    <div class="text-xs text-gray-500">PDFs</div>
                  </div>
                  <div>
                    <div class="text-base font-semibold text-green-600">{{ articleCount }}</div>
                    <div class="text-xs text-gray-500">Articles</div>
                  </div>
                </div>
              </div>

              <div class="space-y-2">
                <BaseButton variant="secondary" size="sm" full-width @click="showUpload = true">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                  </svg>
                  Upload References
                </BaseButton>
                <BaseButton variant="outline" size="sm" full-width @click="router.push('/library')">
                  Browse Library
                </BaseButton>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Recent Activity -->
      <BaseCard variant="elevated" padding="lg" class="bg-gradient-to-r from-orange-50/50 to-blue-50/50">
        <template #header>
          <div class="flex items-center justify-between">
            <div>
              <div class="text-base font-medium text-gray-900">Recent Activity</div>
              <p class="text-gray-600 mt-1">Your latest writing activity</p>
            </div>
            <div class="text-sm text-gray-500">
              Last 7 days
            </div>
          </div>
        </template>
        
        <div class="space-y-4">
          <div class="flex items-center p-3 bg-white/70 rounded-lg">
            <div class="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Research Paper Draft completed</p>
              <p class="text-xs text-gray-500">2 hours ago</p>
            </div>
          </div>
          <div class="flex items-center p-3 bg-white/70 rounded-lg">
            <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">5 new references added to ML Project</p>
              <p class="text-xs text-gray-500">Yesterday</p>
            </div>
          </div>
          <div class="flex items-center p-3 bg-white/70 rounded-lg">
            <div class="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">New project "Data Analysis" created</p>
              <p class="text-xs text-gray-500">3 days ago</p>
            </div>
          </div>
        </div>
      </BaseCard>
    </main>
    <FileUpload :show="showUpload" @close="showUpload = false" @files-selected="uploadFiles" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import BaseCard from '../components/ui/BaseCard.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import FileUpload from '../components/ui/FileUpload.vue'

const router = useRouter()
const userStore = useUserStore()

const showUserMenu = ref(false)
const userMenuRef = ref(null)
const showUpload = ref(false)
const pdfCount = ref(12)
const articleCount = ref(8)

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

// Navigate to project functionality
const navigateToProject = (type) => {
  if (type === 'new') {
    // Navigate to project creation page
    router.push('/project/new')
  } else if (type === 'existing') {
    // Navigate to projects list page
    router.push('/projects')
  }
}

const uploadFiles = async (files) => {
  if (!userStore.token || !files.length) return
  const { useApiStore } = await import('../stores/api')
  const apiStore = useApiStore()
  const axiosInstance = apiStore.createAxiosInstance()
  for (const file of files) {
    const form = new FormData()
    form.append('pdf', file)
    try {
      await axiosInstance.post(`/documents/?token=${userStore.token}`, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      pdfCount.value++
    } catch (err) {
      console.error('Upload failed', err)
    }
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