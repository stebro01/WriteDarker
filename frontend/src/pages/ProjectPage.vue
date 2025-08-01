<template>
  <div class="fit bg-gray-50 column no-wrap overflow-hidden">
    <!-- Header -->
    <PageHeader 
      :title="projectTitle" 
      :show-back-button="true"
      back-route="/dashboard"
    >
      <template #actions>
        <BaseButton variant="outline" size="sm" class="hidden sm:flex">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
          Export
        </BaseButton>
        <!-- Mobile export button -->
        <BaseButton variant="outline" size="sm" class="flex sm:hidden p-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
        </BaseButton>
        <BaseButton variant="primary" size="sm" class="hidden sm:flex">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          Save
        </BaseButton>
        <!-- Mobile save button -->
        <BaseButton variant="primary" size="sm" class="flex sm:hidden p-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
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
          <!-- Document Editor - Always visible -->
          <div :class="documentContainerClasses">
            <DocumentEditor :project-id="projectId" />
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
})

async function loadProjectData() {
  if (!projectId.value) return
  
  try {
    // Load project details
    const projectResult = await projectStore.fetchById(projectId.value)
    if (projectResult.success) {
      currentProject.value = projectResult.data
      console.log('Loaded project:', currentProject.value)
    } else {
      console.error('Failed to load project:', projectResult.error)
    }
    // References and media are now loaded by the sidebars themselves
  } catch (error) {
    console.error('Error loading project data:', error)
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