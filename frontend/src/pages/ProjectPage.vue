<template>
  <div class="h-screen bg-gray-50 flex flex-col overflow-hidden">
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
    <div class="flex-1 flex overflow-hidden">
      <!-- Left Sidebar - References & Files -->
      <div 
        :class="[
          'bg-white border-r border-gray-200 flex flex-col transition-all duration-300',
          leftSidebarCollapsed ? 'w-12' : 'w-80 sm:w-72 lg:w-80'
        ]"
      >
        <!-- Sidebar header -->
        <div class="p-3 border-b border-gray-200 flex items-center justify-between">
          <div v-if="!leftSidebarCollapsed" class="text-xs font-medium text-gray-600 uppercase tracking-wide">References & Files</div>
          <button
            @click="leftSidebarCollapsed = !leftSidebarCollapsed"
            class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="leftSidebarCollapsed ? 'M9 5l7 7-7 7' : 'M15 19l-7-7 7-7'"></path>
            </svg>
          </button>
        </div>

        <!-- Sidebar content -->
        <div v-if="!leftSidebarCollapsed" class="column flex-1 overflow-y-auto min-h-0 sidebar-scrollable">
          <!-- File upload area -->
          <div class="col-auto q-pa-sm">
            <div
              :class="[
                'q-pa-sm border-2 border-dashed text-grey-6 rounded transition-colors',
                isNewProject ? 'cursor-not-allowed opacity-50' : 'cursor-pointer hover:border-orange-6'
              ]"
              style="border-color: #d1d5db;"
              @click="isNewProject ? null : handleDropZoneClick"
              @dragover.prevent="isNewProject ? null : $event"
              @drop.prevent="isNewProject ? null : handleDropZoneDrop"
            >
              <div class="row items-center justify-center q-gutter-x-sm">
                <q-icon name="cloud_upload" size="20px" color="grey-6" />
                <span class="text-caption text-grey-6">
                  {{ isNewProject ? 'Save project first to upload files' : 'Drop files or click' }}
                </span>
              </div>
            </div>
          </div>

          <!-- References and Media Files List -->
          <div class="col">
            <q-list dense class="q-pa-none">
              <ReferenceList
                v-model:expanded="referencesExpanded"
                :references="references"
                @add="showReferenceSearch = true"
                @select="openReference"
              />
              <MediaList
                v-model:expanded="mediaFilesExpanded"
                :media="mediaFiles"
                @select="editMedia"
              />
            </q-list>
          </div>
        </div>

        <!-- Collapsed sidebar icons -->
        <div v-else class="flex-1 flex flex-col items-center py-2 sm:py-4 space-y-2 sm:space-y-3 overflow-y-auto min-h-0">
          <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </button>
          <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Center - Main Document Area -->
      <div class="flex-1 flex flex-col bg-white min-h-0">
        <!-- Document editor -->
        <div class="flex-1 flex flex-col p-4 sm:p-6 min-h-0">
          <div class="max-w-4xl mx-auto flex flex-col flex-1 min-h-0 w-full">
            <!-- Document title -->
            <input
              v-model="documentTitle"
              class="w-full text-sm sm:text-base font-medium text-gray-900 bg-transparent border-none outline-none mb-4 sm:mb-6 placeholder-gray-400 focus:placeholder-gray-300 flex-shrink-0"
              placeholder="Untitled Document"
            />
            
            <!-- Document content -->
            <div class="flex-1 flex flex-col min-h-0">
              <textarea
                v-model="documentContent"
                class="w-full flex-1 min-h-32 resize-none border-none outline-none text-gray-700 placeholder-gray-400 leading-relaxed text-sm focus:placeholder-gray-300"
                placeholder="Start writing your document here..."
              ></textarea>
            </div>
          </div>
        </div>

        <!-- AI Chat section -->
        <div class="border-t border-gray-200 bg-gray-50/50 flex flex-col" :style="chatCollapsed ? 'height: 48px;' : 'height: 200px;'">
          <!-- Chat header -->
          <div class="px-3 sm:px-4 md:px-6 py-2 sm:py-3 bg-white border-b border-gray-200 flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-5 h-5 bg-gradient-to-r from-orange-400 to-orange-600 rounded-full flex items-center justify-center mr-2">
                  <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                <div class="text-xs font-medium text-gray-600 uppercase tracking-wide">AI Assistant</div>
              </div>
              <button
                @click="chatCollapsed = !chatCollapsed"
                class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="chatCollapsed ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Chat messages -->
          <div v-if="!chatCollapsed" class="flex-1 overflow-y-auto p-2 sm:p-3 md:p-4 min-h-0">
            <div class="space-y-3">
              <div
                v-for="message in chatMessages"
                :key="message.id"
                :class="[
                  'flex',
                  message.isUser ? 'justify-end' : 'justify-start'
                ]"
              >
                <div
                  :class="[
                    'max-w-xs sm:max-w-sm lg:max-w-md px-3 py-2 rounded-lg',
                    message.isUser
                      ? 'bg-orange-500 text-white'
                      : 'bg-white border border-gray-200 text-gray-900'
                  ]"
                >
                  <p class="text-xs">{{ message.text }}</p>
                  <p class="text-xs mt-1 opacity-70">{{ message.time }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Chat input -->
          <div v-if="!chatCollapsed" class="p-2 sm:p-3 md:p-4 bg-white border-t border-gray-200 flex-shrink-0">
            <div class="flex space-x-2 sm:space-x-3">
              <input
                v-model="chatInput"
                @keyup.enter="sendMessage"
                class="flex-1 px-3 py-2 text-xs border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Ask AI for help..."
              />
              <BaseButton @click="sendMessage" variant="primary" size="sm" class="flex-shrink-0">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                </svg>
              </BaseButton>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Sidebar - Tools & Options -->
              <div 
          :class="[
            'bg-white border-l border-gray-200 flex flex-col transition-all duration-300',
            rightSidebarCollapsed ? 'w-12' : 'w-80 sm:w-72 lg:w-80'
          ]"
        >
        <template v-if="!rightSidebarCollapsed">
          <!-- Sidebar header -->
          <div class="p-3 border-b border-gray-200 flex items-center justify-between">
            <button
              @click="rightSidebarCollapsed = !rightSidebarCollapsed"
              class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="rightSidebarCollapsed ? 'M15 19l-7-7 7-7' : 'M9 5l7 7-7 7'"></path>
              </svg>
            </button>
            <div class="text-xs font-medium text-gray-600 uppercase tracking-wide">Tools & Options</div>
          </div>

          <!-- Sidebar content -->
          <div class="flex-1 overflow-y-auto min-h-0">
            <q-list dense class="q-pa-none">
              <!-- Project Information section -->
              <q-expansion-item
                v-if="currentProject && !isNewProject"
                v-model="projectInfoExpanded" 
                dense
                expand-separator
                class="text-grey-7"
                style="min-height: 50px;"
              >
                <template v-slot:header>
                  <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
                    Project Information
                  </q-item-section>
                </template>
                
                <div class="q-pa-sm">
                  <!-- Project ID badge with edit button -->
                  <div class="q-mb-sm q-pa-sm bg-blue-1 rounded">
                    <div class="row items-center justify-between">
                      <div class="text-caption text-weight-bold text-blue-9">ID: {{ currentProject.id }}</div>
                      <q-btn
                        flat
                        round
                        dense
                        size="xs"
                        color="blue-7"
                        icon="edit"
                        @click="showProjectEdit = true"
                        class="q-ml-sm"
                      >
                        <q-tooltip class="text-caption">Edit Project</q-tooltip>
                      </q-btn>
                    </div>
                  </div>
                  
                  <!-- Project details -->
                  <div class="column q-gutter-y-xs">
                    <div class="q-pa-xs bg-grey-2 rounded">
                      <div class="text-caption text-weight-bold text-grey-9">{{ currentProject.label }}</div>
                      <div class="text-caption text-grey-6" style="font-size: 10px;">Project Name</div>
                    </div>
                    <div v-if="currentProject.description" class="q-pa-xs bg-grey-2 rounded">
                      <div class="text-caption text-grey-9">{{ currentProject.description }}</div>
                      <div class="text-caption text-grey-6" style="font-size: 10px;">Description</div>
                    </div>
                    <div v-if="currentProject.coauthors" class="q-pa-xs bg-grey-2 rounded">
                      <div class="text-caption text-grey-9">{{ currentProject.coauthors }}</div>
                      <div class="text-caption text-grey-6" style="font-size: 10px;">Co-authors</div>
                    </div>
                  </div>
                </div>
              </q-expansion-item>

              <!-- Document Stats section -->
              <q-expansion-item
                v-model="documentStatsExpanded" 
                dense
                expand-separator
                class="text-grey-7"
                style="min-height: 50px;"
              >
                <template v-slot:header>
                  <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
                    Document Stats
                  </q-item-section>
                </template>
                
                <div class="q-pa-sm">
                  <!-- Main word count -->
                  <div class="q-mb-sm q-pa-sm bg-grey-2 rounded text-center">
                    <div class="text-h6 text-weight-bold text-grey-9">{{ documentStats.words }}</div>
                    <div class="text-caption text-grey-6">Words</div>
                  </div>
                  
                  <!-- Secondary stats -->
                  <div class="row q-gutter-xs">
                    <div class="col q-pa-xs bg-grey-2 rounded text-center">
                      <div class="text-caption text-weight-bold text-grey-9">{{ documentStats.characters }}</div>
                      <div class="text-caption text-grey-6" style="font-size: 10px;">Characters</div>
                    </div>
                    <div class="col q-pa-xs bg-grey-2 rounded text-center">
                      <div class="text-caption text-weight-bold text-grey-9">{{ documentStats.paragraphs }}</div>
                      <div class="text-caption text-grey-6" style="font-size: 10px;">Paragraphs</div>
                    </div>
                  </div>
                </div>
              </q-expansion-item>

              <!-- Writing Tools section -->
              <q-expansion-item
                v-model="writingToolsExpanded"
                dense
                expand-separator
                class="text-grey-7"
                style="min-height: 50px;"
              >
                <template v-slot:header>
                  <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
                    Writing Tools
                  </q-item-section>
                </template>
                
                <div class="q-pa-sm column q-gutter-y-xs">
                  <q-btn 
                    outline
                    dense
                    size="sm"
                    color="grey-7"
                    class="q-py-xs text-caption"
                    icon="spellcheck"
                    label="Grammar Check"
                  />
                  <q-btn 
                    outline
                    dense
                    size="sm"
                    color="grey-7"
                    class="q-py-xs text-caption"
                    icon="auto_fix_high"
                    label="Improve Writing"
                  />
                  <q-btn 
                    outline
                    dense
                    size="sm"
                    color="grey-7"
                    class="q-py-xs text-caption"
                    icon="format_quote"
                    label="Citation Generator"
                  />
                </div>
              </q-expansion-item>

              <!-- Export Options section -->
              <q-expansion-item
                v-model="exportOptionsExpanded"
                dense
                expand-separator
                class="text-grey-7"
                style="min-height: 50px;"
              >
                <template v-slot:header>
                  <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
                    Export Options
                  </q-item-section>
                </template>
                
                <div class="q-pa-sm column q-gutter-y-xs">
                  <q-btn 
                    unelevated
                    dense
                    size="sm"
                    color="orange-6"
                    text-color="white"
                    class="q-py-xs text-caption"
                    icon="picture_as_pdf"
                    label="Export as PDF"
                  />
                  <q-btn 
                    outline
                    dense
                    size="sm"
                    color="grey-7"
                    class="q-py-xs text-caption"
                    icon="description"
                    label="Export as Word"
                  />
                </div>
              </q-expansion-item>
            </q-list>
    </div>

  </template>
        
        <template v-else>
          <!-- Sidebar header collapsed -->
          <div class="p-3 border-b border-gray-200 flex items-center justify-between">
            <button
              @click="rightSidebarCollapsed = !rightSidebarCollapsed"
              class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="rightSidebarCollapsed ? 'M15 19l-7-7 7-7' : 'M9 5l7 7-7 7'"></path>
              </svg>
            </button>
          </div>
          
          <!-- Collapsed sidebar icons -->
          <div class="column items-center q-py-sm q-gutter-y-sm overflow-y-auto min-h-0">
            <q-btn 
              flat
              round
              dense
              size="sm"
              color="grey-6"
              icon="bar_chart"
              class="q-pa-xs"
            />
            <q-btn 
              flat
              round
              dense
              size="sm"
              color="grey-6"
              icon="edit"
              class="q-pa-xs"
            />
              <q-btn
                flat
                round
                dense
                size="sm"
                color="grey-6"
                icon="download"
                class="q-pa-xs"
              />
            </div>
          </template>
        </div>
      </div>
    </div>
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
import ReferenceList from '../components/project/ReferenceList.vue'
import MediaList from '../components/project/MediaList.vue'
import MediaEditDialog from '../components/ui/MediaEditDialog.vue'
import NewProjectDialog from '../components/project/NewProjectDialog.vue'
import ProjectEditDialog from '../components/project/ProjectEditDialog.vue'
import { useReferenceStore } from '../stores/reference'
import { useMediaStore } from '../stores/media'
import { useUserStore } from '../stores/user'
import { useProjectStore } from '../stores/project'

// Stores and routing
const route = useRoute()
const router = useRouter()
const referenceStore = useReferenceStore()
const mediaStore = useMediaStore()
const userStore = useUserStore()
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
const referencesExpanded = ref(true)
const mediaFilesExpanded = ref(true)
const documentStatsExpanded = ref(true)
const writingToolsExpanded = ref(true)
const exportOptionsExpanded = ref(true)
const projectInfoExpanded = ref(true)

// Project data
const projectTitle = computed(() => {
  if (isNewProject.value) {
    return 'New Project'
  }
  return currentProject.value?.label || 'Loading Project...'
})

const documentTitle = ref('The Impact of AI on Modern Writing')
const documentContent = ref('Start writing your document here...')

// Chat functionality
const chatInput = ref('')
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

// File handling
function handleDropZoneClick() {
  droppedFiles.value = []
  showFileAction.value = true
}

function handleDropZoneDrop(e) {
  droppedFiles.value = Array.from(e.dataTransfer.files)
  showFileAction.value = true
}

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

function openReference(ref) {
  if (!ref?.id) return
  window.open(`http://localhost:8000/references/${ref.id}/file?token=${userStore.token}`, '_blank')
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

// Document stats computed property
const documentStats = computed(() => {
  const text = documentContent.value || ''
  const words = text.trim() ? text.trim().split(/\s+/).length : 0
  const characters = text.length
  const paragraphs = text.trim() ? text.split(/\n\s*\n/).length : 0
  
  return { words, characters, paragraphs }
})

// Methods
const sendMessage = () => {
  if (!chatInput.value.trim()) return
  
  const newMessage = {
    id: Date.now(),
    text: chatInput.value,
    isUser: true,
    time: 'now'
  }
  
  chatMessages.value.push(newMessage)
  chatInput.value = ''
  
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