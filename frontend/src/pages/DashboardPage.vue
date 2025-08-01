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
          <p class="text-gray-600 mb-4">Ready to continue your writing journey?</p>
          
          <!-- Recent Project Button -->
          <BaseButton 
            v-if="projectStore.recentProject"
            @click="openRecentProject"
            variant="primary" 
            size="md"
            class="hover:shadow-lg transition-all duration-300"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Continue with "{{ projectStore.recentProject.label }}"
          </BaseButton>
          
          <BaseButton 
            v-else
            @click="navigateToProject('new')"
            variant="primary" 
            size="md"
            class="hover:shadow-lg transition-all duration-300"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Create Your First Project
          </BaseButton>
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
            
            <BaseButton 
              @click="router.push('/user-details')"
              variant="outline" 
              size="sm" 
              full-width
              class="mt-4 group-hover:shadow-md transition-shadow"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
              </svg>
              Edit Details
            </BaseButton>
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
                  <span class="text-sm font-medium text-gray-700">Total Projects</span>
                  <span class="text-base font-semibold text-blue-600">{{ totalProjects }}</span>
                </div>
                <div class="text-xs text-gray-500 space-y-1">
                  <div class="flex justify-between mb-2">
                    <span class="font-medium text-gray-700">By Progress:</span>
                  </div>
                  <div v-if="completedProjects > 0" class="flex justify-between">
                    <span>Completed:</span>
                    <span class="font-medium text-green-600">{{ completedProjects }}</span>
                  </div>
                  <div v-if="inProgressProjects > 0" class="flex justify-between">
                    <span>In Progress:</span>
                    <span class="font-medium text-orange-600">{{ inProgressProjects }}</span>
                  </div>
                  <div v-if="emptyProjects > 0" class="flex justify-between">
                    <span>Empty:</span>
                    <span class="font-medium text-gray-600">{{ emptyProjects }}</span>
                  </div>
                  
                  <div class="flex justify-between mt-3 mb-2">
                    <span class="font-medium text-gray-700">By Status:</span>
                  </div>
                  <div v-if="activeProjects > 0" class="flex justify-between">
                    <span>Active:</span>
                    <span class="font-medium text-blue-600">{{ activeProjects }}</span>
                  </div>
                  <div v-if="waitingProjects > 0" class="flex justify-between">
                    <span>Waiting:</span>
                    <span class="font-medium text-yellow-600">{{ waitingProjects }}</span>
                  </div>
                  <div v-if="finishedProjects > 0" class="flex justify-between">
                    <span>Finished:</span>
                    <span class="font-medium text-green-600">{{ finishedProjects }}</span>
                  </div>
                </div>
              </div>
              
              <div class="space-y-2">
                <BaseButton 
                  @click="navigateToProject('existing')"
                  variant="outline" 
                  size="sm" 
                  full-width
                >
                  View All Projects
                </BaseButton>
                <BaseButton 
                  @click="navigateToProject('new')"
                  variant="primary" 
                  size="sm" 
                  full-width
                  class="group-hover:shadow-md transition-shadow q-mt-xs"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                  New Project
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
                <BaseButton class="q-mt-xs" variant="outline" size="sm" full-width @click="router.push('/library')">
                  Browse Library
                </BaseButton>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Writing Hub -->
      <BaseCard variant="elevated" padding="lg" class="bg-gradient-to-r from-orange-50/50 to-blue-50/50">
        <template #header>
          <div class="flex items-center justify-between">
            <div>
              <div class="text-base font-medium text-gray-900">Writing Hub</div>
              <p class="text-gray-600 mt-1">Inspiration and quick actions for your writing journey</p>
            </div>
            <div class="flex items-center text-orange-500">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
          </div>
        </template>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Daily Inspiration -->
          <div class="space-y-4">
            <div class="bg-white/70 rounded-lg p-4">
              <div class="flex items-center mb-3">
                <div class="w-8 h-8 bg-gradient-to-r from-purple-400 to-purple-600 rounded-full flex items-center justify-center mr-3">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                <h3 class="font-medium text-gray-900">Daily Inspiration</h3>
              </div>
              <blockquote class="text-sm text-gray-700 italic mb-2">
                "{{ currentTip.quote }}"
              </blockquote>
              <p class="text-xs text-gray-500">— {{ currentTip.author }}</p>
            </div>

            <!-- Writing Statistics -->
            <div class="bg-white/70 rounded-lg p-4">
              <h3 class="font-medium text-gray-900 mb-3 flex items-center">
                <div class="w-8 h-8 bg-gradient-to-r from-green-400 to-green-600 rounded-full flex items-center justify-center mr-3">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                </div>
                Your Progress
              </h3>
              <div class="grid grid-cols-2 gap-3 text-sm">
                <div class="text-center">
                  <div class="font-semibold text-blue-600">{{ totalProjects }}</div>
                  <div class="text-xs text-gray-500">Projects</div>
                </div>
                <div class="text-center">
                  <div class="font-semibold text-green-600">{{ pdfCount + articleCount }}</div>
                  <div class="text-xs text-gray-500">References</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="space-y-4">
            <div class="bg-white/70 rounded-lg p-4">
              <h3 class="font-medium text-gray-900 mb-3 flex items-center">
                <div class="w-8 h-8 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full flex items-center justify-center mr-3">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                </div>
                Quick Actions
              </h3>
              <div class="space-y-2">
                <BaseButton 
                  @click="quickCreateDocument"
                  variant="outline" 
                  size="sm" 
                  full-width
                  class="justify-start"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                  Quick Document
                </BaseButton>
                <BaseButton 
                  @click="showUpload = true"
                  variant="outline" 
                  size="sm" 
                  full-width
                  class="justify-start"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                  </svg>
                  Add References
                </BaseButton>
                <BaseButton 
                  @click="router.push('/library')"
                  variant="outline" 
                  size="sm" 
                  full-width
                  class="justify-start"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                  Browse Library
                </BaseButton>
              </div>
            </div>

            <!-- Writing Tip -->
            <div class="bg-white/70 rounded-lg p-4">
              <h3 class="font-medium text-gray-900 mb-2 flex items-center">
                <div class="w-8 h-8 bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center mr-3">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                  </svg>
                </div>
                Writing Tip
              </h3>
              <p class="text-sm text-gray-700">{{ currentTip.tip }}</p>
            </div>
          </div>
        </div>
      </BaseCard>
    </main>
    <FileUpload :show="showUpload" @close="showUpload = false" @files-selected="uploadFiles" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useReferenceStore } from '../stores/reference'
import { useProjectStore } from '../stores/project'
import BaseCard from '../components/ui/BaseCard.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import FileUpload from '../components/ui/FileUpload.vue'

const router = useRouter()
const userStore = useUserStore()
const referenceStore = useReferenceStore()
const projectStore = useProjectStore()

const showUserMenu = ref(false)
const userMenuRef = ref(null)
const showUpload = ref(false)
const pdfCount = computed(() => referenceStore.pdfCount)
const articleCount = computed(() => referenceStore.referenceCount)

// Project statistics computed properties
const totalProjects = computed(() => projectStore.projects.length)
const emptyProjects = computed(() => 
  projectStore.projects.filter(project => project.document_count === 0).length
)
const inProgressProjects = computed(() => 
  projectStore.projects.filter(project => 
    project.document_count > 0 && project.word_count > 0 && project.word_count < 1000
  ).length
)
const completedProjects = computed(() => 
  projectStore.projects.filter(project => project.word_count >= 1000).length
)

// Project status computed properties
const activeProjects = computed(() => 
  projectStore.projects.filter(project => project.status === 'active').length
)
const waitingProjects = computed(() => 
  projectStore.projects.filter(project => project.status === 'waiting').length
)
const finishedProjects = computed(() => 
  projectStore.projects.filter(project => project.status === 'finished').length
)

// Writing tips and inspiration
const writingTips = [
  {
    quote: "The first draft of anything is shit.",
    author: "Ernest Hemingway",
    tip: "Don't aim for perfection in your first draft. Just get your ideas down on paper."
  },
  {
    quote: "You can always edit a bad page. You can't edit a blank page.",
    author: "Jodi Picoult",
    tip: "Set a daily writing goal, even if it's just 100 words. Consistency beats perfection."
  },
  {
    quote: "Start writing, no matter what. The water does not flow until the faucet is turned on.",
    author: "Louis L'Amour",
    tip: "Use the Pomodoro technique: write for 25 minutes, then take a 5-minute break."
  },
  {
    quote: "If you want to be a writer, you must do two things above all others: read a lot and write a lot.",
    author: "Stephen King",
    tip: "Keep a notebook with you. Great ideas often come when you least expect them."
  },
  {
    quote: "The secret to getting ahead is getting started.",
    author: "Mark Twain",
    tip: "Break large writing projects into smaller, manageable sections. Tackle one at a time."
  },
  {
    quote: "Write drunk, edit sober.",
    author: "Attributed to Hemingway",
    tip: "Let your creativity flow freely in the first draft, then refine with a critical eye."
  }
]

const currentTip = computed(() => {
  const dayOfYear = Math.floor((Date.now() - new Date(new Date().getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24))
  return writingTips[dayOfYear % writingTips.length]
})

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

// Open recent project
const openRecentProject = () => {
  if (projectStore.recentProject) {
    router.push(`/project/${projectStore.recentProject.id}`)
  }
}

// Quick create document
const quickCreateDocument = async () => {
  // If user has a recent project, create document in that project
  if (projectStore.recentProject) {
    router.push(`/project/${projectStore.recentProject.id}`)
  } else if (projectStore.projects.length > 0) {
    // Navigate to the most recent project
    const mostRecentProject = projectStore.projects[0]
    router.push(`/project/${mostRecentProject.id}`)
  } else {
    // No projects exist, prompt to create one first
    router.push('/project/new')
  }
}

const uploadFiles = async (files) => {
  if (!files.length) return
  for (const file of files) {
    const result = await referenceStore.upload({ query: file.name, file })
    if (!result.success) {
      if (result.isDuplicate) {
        // Show user-friendly duplicate message
        alert(`Duplicate file: ${result.error}`)
      } else {
        console.error('Upload failed:', result.error)
        alert(`Upload failed: ${result.error}`)
      }
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
  referenceStore.fetchAll()
  projectStore.fetchAll()
  projectStore.fetchRecentProject()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>