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
        @show-file-action="showFileAction = true"
        @show-reference-search="showReferenceSearch = true"
        @edit-media="editMedia"

        style="height: calc(100vh - 60px);"
      />

      <!-- Center - Main Document Area -->
      <div class="col column bg-white" style="height: calc(100vh - 60px);">
        <!-- Document editor with scroll area -->
        <div class="col column">
          <DocumentEditor
            :project-id="projectId"
          />
        </div>

        <!-- AI Chat section - fixed height -->
        <div class="col-auto">
          <AiAssistant
            :collapsed="chatCollapsed"
            :messages="chatMessages"
            @toggle-collapse="chatCollapsed = !chatCollapsed"
            @send-message="sendMessage"
          />
        </div>
      </div>

      <!-- Right Sidebar - Tools & Options -->
      <RightSidebar
        :collapsed="rightSidebarCollapsed"
        :current-project="currentProject"
        :is-new-project="isNewProject"
        :project-id="projectId"
        @toggle-collapse="rightSidebarCollapsed = !rightSidebarCollapsed"
        @edit-project="showProjectEdit = true"
        style="height: calc(100vh - 60px);"
      />
    </div>

    <!-- Dialogs -->
    <FileActionDialog
      :show="showFileAction"
      @close="showFileAction = false"
      @upload-pdf="handleUploadPdf"
      @search-pubmed="handleSearchPubMed"
      @upload-media="handleUploadMedia"
    />

    <FileUpload
      :show="showPdfUpload"
      accept=".pdf"
      @close="showPdfUpload = false"
      @files-selected="uploadPdfFiles"
    />

    <FileUpload
      :show="showMediaUpload"
      accept="image/*,audio/*,video/*"
      @close="showMediaUpload = false"
      @files-selected="uploadMediaFiles"
    />

    <PubMedSearch
      :show="showPubMedSearch"
      @close="showPubMedSearch = false"
    />

    <ReferenceSearchDialog
      v-if="projectId"
      :show="showReferenceSearch"
      :project-id="projectId"
      @close="showReferenceSearch = false"
      @added="handleReferenceAdded"
    />

    <MediaEditDialog
      :show="showMediaEdit"
      :media="selectedMedia"
      @close="showMediaEdit = false"
      @updated="handleMediaUpdated"
    />

    <NewProjectDialog
      :show="showNewProject"
      @close="handleNewProjectClose"
      @created="handleProjectCreated"
    />

    <ProjectEditDialog
      :show="showProjectEdit"
      :project="currentProject"
      @close="showProjectEdit = false"
      @updated="handleProjectUpdated"
      @deleted="handleProjectDeleted"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseButton from '../components/ui/BaseButton.vue'
import PageHeader from '../components/ui/PageHeader.vue'
import FileActionDialog from '../components/project/FileActionDialog.vue'
import FileUpload from '../components/ui/FileUpload.vue'
import PubMedSearch from '../components/ui/PubMedSearch.vue'
import ReferenceSearchDialog from '../components/project/ReferenceSearchDialog.vue'
import MediaEditDialog from '../components/ui/MediaEditDialog.vue'
import NewProjectDialog from '../components/project/NewProjectDialog.vue'
import ProjectEditDialog from '../components/project/ProjectEditDialog.vue'
import LeftSidebar from '../components/project/sidebar/LeftSidebar.vue'
import DocumentEditor from '../components/project/editor/DocumentEditor.vue'
import AiAssistant from '../components/project/chat/AiAssistant.vue'
import RightSidebar from '../components/project/sidebar/RightSidebar.vue'
import { useReferenceStore } from '../stores/reference'
import { useMediaStore } from '../stores/media'
import { useProjectStore } from '../stores/project'

// Stores and routing
const route = useRoute()
const router = useRouter()
const referenceStore = useReferenceStore()
const mediaStore = useMediaStore()
const projectStore = useProjectStore()

// Dialog states
const showFileAction = ref(false)
const showPdfUpload = ref(false)
const showMediaUpload = ref(false)
const showPubMedSearch = ref(false)
const showReferenceSearch = ref(false)
const showMediaEdit = ref(false)
const showNewProject = ref(false)
const showProjectEdit = ref(false)
const selectedMedia = ref(null)
const droppedFiles = ref([])

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

const references = computed(() => referenceStore.references)
const mediaFiles = computed(() => mediaStore.media)

// File handling - shared between components

// Note: Drag and drop functionality removed in favor of button-based file selection

async function handleUploadPdf() {
  if (droppedFiles.value.length) {
    await uploadPdfFiles(droppedFiles.value)
    droppedFiles.value = []
    showFileAction.value = false
  } else {
    showFileAction.value = false
    showPdfUpload.value = true
  }
}

async function uploadPdfFiles(files) {
  for (const file of files) {
    await referenceStore.upload({
      projectIds: projectId.value ? [projectId.value] : [],
      query: file.name,
      file
    })
  }
}

function handleSearchPubMed() {
  showFileAction.value = false
  showPubMedSearch.value = true
}

async function handleUploadMedia() {
  if (droppedFiles.value.length) {
    await uploadMediaFiles(droppedFiles.value)
    droppedFiles.value = []
    showFileAction.value = false
  } else {
    showFileAction.value = false
    showMediaUpload.value = true
  }
}

async function uploadMediaFiles(files) {
  if (!projectId.value) {
    if (isNewProject.value) {
      console.error('Cannot upload media files to a new project. Please save the project first.')
      // TODO: Show user-friendly notification that project needs to be saved first
      alert('Please save your project before uploading media files.')
      return
    } else {
      console.error('No project ID available for media upload')
      return
    }
  }
  
  console.log('Starting media upload for', files.length, 'files')
  
  let successCount = 0
  let errorCount = 0
  
  for (const file of files) {
    console.log('Uploading file:', file.name, 'Type:', file.type, 'Size:', file.size)
    try {
      const result = await mediaStore.upload({ 
        projectId: projectId.value, 
        file, 
        label: file.name 
      })
      
      if (result.success) {
        console.log('Upload successful for:', file.name)
        successCount++
      } else {
        console.error('Upload failed for:', file.name, 'Error:', result.error)
        errorCount++
      }
    } catch (error) {
      console.error('Upload error for:', file.name, error)
      errorCount++
    }
  }
  
  // Show summary
  console.log(`Upload complete: ${successCount} successful, ${errorCount} failed`)
  
  // Refresh the media list after upload
  if (projectId.value && successCount > 0) {
    try {
      await mediaStore.fetch(projectId.value)
      console.log('Media list refreshed')
    } catch (error) {
      console.error('Failed to refresh media list:', error)
    }
  }
}

function editMedia(media) {
  if (!media) return
  selectedMedia.value = media
  showMediaEdit.value = true
}

async function handleMediaUpdated() {
  if (projectId.value) {
    await mediaStore.fetch(projectId.value)
  }
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

    // Load references and media in parallel
    await Promise.all([
      referenceStore.fetchAll(projectId.value),
      mediaStore.fetch(projectId.value)
    ])
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

async function handleReferenceAdded() {
  if (projectId.value) {
    await referenceStore.fetchAll(projectId.value)
  }
}

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
</style>