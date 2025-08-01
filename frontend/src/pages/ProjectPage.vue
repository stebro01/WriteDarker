<template>
  <div class="fit bg-gray-50 column no-wrap overflow-hidden">
    <!-- Header -->
    <PageHeader 
      :title="projectTitle" 
      :show-back-button="true"
      back-route="/dashboard"
    >
      <template #actions>
        <!-- Search -->
        <BaseButton variant="ghost" size="sm" @click="toggleSearch" :disabled="!currentProject">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          Search
        </BaseButton>

        <!-- Auto-save Indicator -->
        <BaseButton 
          variant="ghost" 
          size="sm" 
          :class="{
            'text-green-600': autoSaveStatus === 'saved',
            'text-blue-600': autoSaveStatus === 'saving',
            'text-orange-600': autoSaveStatus === 'unsaved',
            'text-red-600': autoSaveStatus === 'error'
          }"
          :disabled="true"
        >
          <svg v-if="autoSaveStatus === 'saved'" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else-if="autoSaveStatus === 'saving'" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          <svg v-else-if="autoSaveStatus === 'unsaved'" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.996-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
          <svg v-else-if="autoSaveStatus === 'error'" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ autoSaveStatusText }}
        </BaseButton>
      </template>
    </PageHeader>

    <!-- Main content area -->
    <div class="col row no-wrap overflow-hidden">
      <!-- Left Sidebar - References & Files -->
      <LeftSidebar
        :collapsed="leftSidebarCollapsed"
        :project-id="projectId"
        :is-new-project="isNewProject"
        :references="references"
        :media-files="mediaFiles"
        @toggle-collapse="leftSidebarCollapsed = !leftSidebarCollapsed"
        @media-updated="handleMediaUpdated"
        @reference-added="handleReferenceAdded"
        style="height: calc(100vh - 60px);"
      />

      <!-- Center - Main Document Area -->
      <div class="col column bg-white" style="height: calc(100vh - 60px);">
        <!-- Flexible Layout Container -->
        <div class="column" style="height: calc(100vh - 60px);">
          <!-- Document Editor - Only visible when we have a valid project -->
          <div v-if="projectId" :class="documentContainerClasses">
            <DocumentEditor :project-id="projectId" />
          </div>
          
          <!-- New Project Placeholder - Show when creating new project -->
          <div v-else-if="isNewProject" class="flex items-center justify-center h-full bg-gray-50">
            <div class="text-center">
              <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Create a New Project</h3>
              <p class="text-gray-600 mb-4">Fill in the project details in the dialog to get started</p>
            </div>
          </div>
          
          <!-- Splitter Handle - Only when AI is expanded -->
          <div 
            v-if="!chatCollapsed"
            class="splitter-handle"
            @mousedown="startResize"
          >
            <div class="splitter-line"></div>
          </div>
          
          <!-- AI Assistant - Always present but variable height -->
          <div :class="aiContainerClasses" :style="aiContainerStyle">
            <AiAssistant
              :collapsed="chatCollapsed"
              :messages="chatMessages"
              @toggle-collapse="chatCollapsed = !chatCollapsed"
              @send-message="sendMessage"
            />
          </div>
        </div>
      </div>

      <!-- Right Sidebar - Tools & Options -->
      <RightSidebar
        :collapsed="rightSidebarCollapsed"
        :current-project="currentProject"
        :is-new-project="isNewProject"
        :project-id="projectId"
        @toggle-collapse="rightSidebarCollapsed = !rightSidebarCollapsed"
        @project-updated="handleProjectUpdated"
        @project-deleted="handleProjectDeleted"
        style="height: calc(100vh - 60px);"
      />
    </div>

    <!-- Search Dialog -->
    <div 
      v-if="showSearchDialog" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center pt-20 z-50"
      @click.self="showSearchDialog = false"
    >
      <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4">
        <!-- Search Header -->
        <div class="p-4 border-b border-gray-200">
          <div class="flex items-center space-x-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input
              v-model="searchQuery"
              @input="performSearch"
              @keydown.esc="showSearchDialog = false"
              class="search-input flex-1 text-lg border-none outline-none placeholder-gray-400"
              placeholder="Search across all documents..."
              type="text"
            />
            <button
              @click="showSearchDialog = false"
              class="p-1 text-gray-400 hover:text-gray-600 rounded"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Search Results -->
        <div class="max-h-96 overflow-y-auto">
          <div v-if="searchQuery.trim() && searchResults.length === 0" class="p-8 text-center text-gray-500">
            No results found for "{{ searchQuery }}"
          </div>
          <div v-else-if="!searchQuery.trim()" class="p-8 text-center text-gray-400">
            Start typing to search across all documents...
          </div>
          <div v-else>
            <div
              v-for="result in searchResults"
              :key="result.document.id"
              class="p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer"
              @click="openSearchResult(result)"
            >
              <div class="font-medium text-gray-900 mb-1">
                {{ result.document.title }}
                <span v-if="result.titleMatch" class="ml-2 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                  Title match
                </span>
              </div>
              <div v-if="result.context" class="text-sm text-gray-600">
                {{ result.context }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- Search Footer -->
        <div v-if="searchResults.length > 0" class="p-3 bg-gray-50 text-xs text-gray-500 border-t border-gray-200">
          {{ searchResults.length }} result{{ searchResults.length !== 1 ? 's' : '' }} found
        </div>
      </div>
    </div>

    <!-- Dialogs -->
    <NewProjectDialog
      :show="showNewProject"
      @close="handleNewProjectClose"
      @created="handleProjectCreated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseButton from '../components/ui/BaseButton.vue'
import PageHeader from '../components/ui/PageHeader.vue'
import NewProjectDialog from '../components/project/NewProjectDialog.vue'
import LeftSidebar from '../components/project/sidebar/LeftSidebar.vue'
import DocumentEditor from '../components/project/editor/DocumentEditor.vue'
import AiAssistant from '../components/project/chat/AiAssistant.vue'
import RightSidebar from '../components/project/sidebar/RightSidebar.vue'
import { useProjectStore } from '../stores/project'

// Stores and routing
const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

// Dialog states
const showNewProject = ref(false)

// Custom splitter state
const aiPanelHeight = ref(300) // Default height in pixels when expanded
const isResizing = ref(false)

// Header functionality states
const showSearchDialog = ref(false)
const searchQuery = ref('')
const searchResults = ref([])

// Auto-save state
const autoSaveStatus = ref('saved') // 'saved', 'saving', 'unsaved', 'error'
const lastSaveTime = ref(null)

const projectId = computed(() => {
  const id = route.params.id
  console.log('ProjectPage route params:', route.params)
  console.log('Extracted project ID:', id)
  console.log('Current route path:', route.path)
  return id ? parseInt(id, 10) : null
})

const isNewProject = computed(() => route.path === '/project/new')

// Current project data
const currentProject = ref(null)

// Sidebar states
const leftSidebarCollapsed = ref(false)
const rightSidebarCollapsed = ref(false)
const chatCollapsed = ref(false)

// Project data
const projectTitle = computed(() => {
  if (isNewProject.value) {
    return 'New Project'
  }
  return currentProject.value?.label || 'Loading Project...'
})

// Document management is now handled by DocumentListEditor component

// Chat functionality
const chatMessages = ref([
  {
    id: 1,
    text: 'Hi! I\'m here to help you with your writing. What would you like to work on?',
    isUser: false,
    time: '2 min ago'
  },
  {
    id: 2,
    text: 'Can you help me improve this introduction?',
    isUser: true,
    time: '1 min ago'
  },
  {
    id: 3,
    text: 'Of course! I\'d be happy to help you improve your introduction. Please share the text you\'d like me to review.',
    isUser: false,
    time: '30 sec ago'
  }
])

// References and media will be loaded by the sidebars themselves
const references = ref([])
const mediaFiles = ref([])

// Project documents for statistics and search
const projectDocuments = ref([])

// Layout computed properties
const documentContainerClasses = computed(() => {
  return chatCollapsed.value ? 'col' : 'column-content'
})

const aiContainerClasses = computed(() => {
  return chatCollapsed.value ? 'col-auto' : 'ai-panel-expanded'
})

const aiContainerStyle = computed(() => {
  if (chatCollapsed.value) {
    return {}
  }
  return {
    height: `${aiPanelHeight.value}px`,
    minHeight: '200px',
    maxHeight: '600px'
  }
})

// Auto-save computed
const autoSaveStatusText = computed(() => {
  switch (autoSaveStatus.value) {
    case 'saved':
      return lastSaveTime.value ? `Saved ${formatTimeAgo(lastSaveTime.value)}` : 'Saved'
    case 'saving':
      return 'Saving...'
    case 'unsaved':
      return 'Unsaved changes'
    case 'error':
      return 'Save failed'
    default:
      return 'Unknown'
  }
})



// Event handlers for sidebar events
function handleMediaUpdated() {
  // Media updates are now handled by LeftSidebar
  console.log('Media updated')
}

function handleReferenceAdded() {
  // Reference additions are now handled by LeftSidebar
  console.log('Reference added')
}

// Custom splitter methods
function startResize(event) {
  isResizing.value = true
  const startY = event.clientY
  const startHeight = aiPanelHeight.value

  function handleMouseMove(e) {
    if (!isResizing.value) return
    
    const deltaY = startY - e.clientY // Inverted because we want drag up to increase height
    const newHeight = Math.max(200, Math.min(600, startHeight + deltaY))
    aiPanelHeight.value = newHeight
  }

  function handleMouseUp() {
    isResizing.value = false
    document.removeEventListener('mousemove', handleMouseMove)
    document.removeEventListener('mouseup', handleMouseUp)
  }

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

// Helper functions
function formatTimeAgo(timestamp) {
  if (!timestamp) return 'recently'
  
  const now = new Date()
  const diff = Math.floor((now - timestamp) / 1000)
  
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

// Search functionality
function toggleSearch() {
  showSearchDialog.value = !showSearchDialog.value
  
  if (showSearchDialog.value) {
    // Focus search input after dialog opens
    setTimeout(() => {
      const searchInput = document.querySelector('.search-input')
      if (searchInput) searchInput.focus()
    }, 100)
  }
}

function performSearch() {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }
  
  const query = searchQuery.value.toLowerCase()
  const results = []
  
  projectDocuments.value.forEach(doc => {
    const text = (doc.text || doc.content || '').toLowerCase()
    const title = (doc.title || doc.label || '').toLowerCase()
    
    if (title.includes(query) || text.includes(query)) {
      // Find context around matches
      const textIndex = text.indexOf(query)
      const titleMatch = title.includes(query)
      
      let context = ''
      if (textIndex !== -1) {
        const start = Math.max(0, textIndex - 50)
        const end = Math.min(text.length, textIndex + query.length + 50)
        context = text.substring(start, end)
        if (start > 0) context = '...' + context
        if (end < text.length) context = context + '...'
      }
      
      results.push({
        document: doc,
        titleMatch,
        context,
        matchIndex: textIndex
      })
    }
  })
  
  searchResults.value = results
}

// Auto-save simulation
function simulateAutoSave() {
  // This would normally be triggered by document changes
  autoSaveStatus.value = 'saving'
  
  setTimeout(() => {
    // Simulate successful save
    autoSaveStatus.value = 'saved'
    lastSaveTime.value = new Date()
  }, 1000)
}



// Methods
const sendMessage = (messageText) => {
  if (!messageText?.trim()) return
  
  const newMessage = {
    id: Date.now(),
    text: messageText,
    isUser: true,
    time: 'now'
  }
  
  chatMessages.value.push(newMessage)
  
  // Simulate AI response
  setTimeout(() => {
    const aiResponse = {
      id: Date.now() + 1,
      text: 'I understand your question. Let me help you with that...',
      isUser: false,
      time: 'now'
    }
    chatMessages.value.push(aiResponse)
  }, 1000)
}

onMounted(async () => {
  if (projectId.value) {
    // Load project data and related items
    await loadProjectData()
  } else if (isNewProject.value) {
    // Show new project dialog when on /project/new route
    showNewProject.value = true
  }
  
  // Add keyboard shortcuts
  const handleKeydown = (event) => {
    // Ctrl+K or Cmd+K to open search
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
      event.preventDefault()
      if (currentProject.value) {
        toggleSearch()
      }
    }
    // Escape to close search
    if (event.key === 'Escape' && showSearchDialog.value) {
      showSearchDialog.value = false
    }
  }
  
  document.addEventListener('keydown', handleKeydown)
  
  // Cleanup on unmount
  return () => {
    document.removeEventListener('keydown', handleKeydown)
  }
})

async function loadProjectData() {
  if (!projectId.value) return
  
  try {
    // Load project details
    const projectResult = await projectStore.fetchById(projectId.value)
    if (projectResult.success) {
      currentProject.value = projectResult.data
      console.log('Loaded project:', currentProject.value)
      
      // Load project documents for statistics and search
      await loadProjectDocuments()
    } else {
      console.error('Failed to load project:', projectResult.error)
    }
    // References and media are now loaded by the sidebars themselves
  } catch (error) {
    console.error('Error loading project data:', error)
  }
}

async function loadProjectDocuments() {
  if (!projectId.value) return
  
  try {
    // This would normally make an API call to get documents for this project
    // For now, we'll simulate some documents
    projectDocuments.value = [
      {
        id: 1,
        title: 'Introduction',
        text: 'This is the introduction section of our project. It contains important background information and sets the context for our research.',
        created_at: new Date('2024-01-15')
      },
      {
        id: 2,
        title: 'Literature Review',
        text: 'Here we review the existing literature in the field. Many researchers have contributed to this area of study over the years.',
        created_at: new Date('2024-01-16')
      },
      {
        id: 3,
        title: 'Methodology',
        text: 'Our research methodology follows a systematic approach. We employ both qualitative and quantitative methods to ensure comprehensive analysis.',
        created_at: new Date('2024-01-17')
      }
    ]
    
    // Set initial auto-save status
    autoSaveStatus.value = 'saved'
    lastSaveTime.value = new Date()
    
    // Demo: Simulate some auto-save activity after a delay
    setTimeout(() => {
      simulateAutoSave()
    }, 3000)
  } catch (error) {
    console.error('Error loading project documents:', error)
  }
}

// Watch for route changes to handle new project dialog and project changes
watch(() => route.path, (newPath) => {
  if (newPath === '/project/new') {
    showNewProject.value = true
    currentProject.value = null
  }
}, { immediate: true })

// Watch for project ID changes to reload data
watch(() => projectId.value, async (newProjectId, oldProjectId) => {
  if (newProjectId && newProjectId !== oldProjectId) {
    await loadProjectData()
  }
})

// Watch for search query changes
watch(() => searchQuery.value, () => {
  performSearch()
})

function handleNewProjectClose() {
  showNewProject.value = false
  // If user cancels new project creation, redirect to dashboard
  // since they can't stay on /project/new without a project
  if (isNewProject.value) {
    router.push('/dashboard')
  }
}

async function handleProjectCreated(project) {
  console.log('Project created:', project)
  // Navigate to the new project page
  showNewProject.value = false
  await router.push(`/project/${project.id}`)
}

async function handleProjectUpdated(updatedProject) {
  console.log('Project updated:', updatedProject)
  // Update the current project data
  currentProject.value = updatedProject
}

async function handleProjectDeleted(deletedProject) {
  console.log('Project deleted:', deletedProject)
  // Navigate back to dashboard
  await router.push('/dashboard')
}

function openSearchResult(result) {
  console.log('Opening search result:', result)
  // This would navigate to or highlight the specific document
  // For now, just close the search dialog
  showSearchDialog.value = false
  
  // TODO: Implement navigation to specific document or scroll to match
}
</script>

<style scoped>
textarea {
  font-family: inherit;
  line-height: 1.75;
  color: #374151;
}

/* Custom layout classes */
.column-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-panel-expanded {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Custom splitter handle */
.splitter-handle {
  height: 4px;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  cursor: row-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
  user-select: none;
}

.splitter-handle:hover {
  background: #e8e8e8;
}

.splitter-line {
  width: 40px;
  height: 2px;
  background: #c0c0c0;
  border-radius: 1px;
}

.splitter-handle:hover .splitter-line {
  background: #999;
}
</style>