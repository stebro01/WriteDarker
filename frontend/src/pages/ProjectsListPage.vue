<template>
  <div class="h-screen bg-gray-50 flex flex-col overflow-hidden">
    <!-- Header -->
    <PageHeader 
      title="My Projects" 
      :show-back-button="true"
      back-route="/dashboard"
    >
      <template #actions>
        <BaseButton variant="primary" size="sm" @click="createNewProject">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          New Project
        </BaseButton>
      </template>
    </PageHeader>

    <!-- Main content -->
    <div class="flex-1 overflow-auto p-6">
      <div class="max-w-6xl mx-auto">
        <!-- Stats Overview -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
              </div>
              <div>
                <div class="text-2xl font-bold text-gray-900">{{ totalProjects }}</div>
                <div class="text-sm text-gray-600">Total Projects</div>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div>
                <div class="text-2xl font-bold text-gray-900">{{ activeProjects }}</div>
                <div class="text-sm text-gray-600">Active</div>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div>
                <div class="text-2xl font-bold text-gray-900">{{ inProgressProjects }}</div>
                <div class="text-sm text-gray-600">In Progress</div>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
              </div>
              <div>
                <div class="text-2xl font-bold text-gray-900">{{ completedProjects }}</div>
                <div class="text-sm text-gray-600">Completed</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Search and Filter -->
        <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200 mb-6">
          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex-1">
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Search projects..." 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
            </div>
            <div class="flex gap-2">
              <select 
                v-model="statusFilter" 
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="in-progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="archived">Archived</option>
              </select>
              <select 
                v-model="sortBy" 
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                <option value="updated">Last Updated</option>
                <option value="created">Date Created</option>
                <option value="name">Project Name</option>
                <option value="status">Status</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Projects Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="project in filteredProjects" 
            :key="project.id"
            class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200 cursor-pointer"
            @click="openProject(project)"
          >
            <!-- Project Header -->
            <div class="p-4 border-b border-gray-100">
              <div class="flex items-start justify-between mb-2">
                <h3 class="text-lg font-medium text-gray-900 truncate">{{ project.title }}</h3>
                <div class="flex items-center space-x-2">
                  <span 
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      getStatusClasses(project.status)
                    ]"
                  >
                    {{ getStatusLabel(project.status) }}
                  </span>
                  <button 
                    @click.stop="showProjectMenu(project, $event)"
                    class="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <p class="text-sm text-gray-600 line-clamp-2">{{ project.description || 'No description available' }}</p>
            </div>

            <!-- Project Stats -->
            <div class="p-4">
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="text-center">
                  <div class="text-lg font-semibold text-gray-900">{{ project.wordCount || 0 }}</div>
                  <div class="text-xs text-gray-500">Words</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-semibold text-gray-900">{{ project.referenceCount || 0 }}</div>
                  <div class="text-xs text-gray-500">References</div>
                </div>
              </div>

              <!-- Progress Bar -->
              <div class="mb-4">
                <div class="flex justify-between text-xs text-gray-500 mb-1">
                  <span>Progress</span>
                  <span>{{ project.progress || 0 }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-gradient-to-r from-orange-400 to-orange-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${project.progress || 0}%` }"
                  ></div>
                </div>
              </div>

              <!-- Project Meta -->
              <div class="flex items-center justify-between text-xs text-gray-500">
                <div class="flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  {{ formatDate(project.updatedAt || project.createdAt) }}
                </div>
                <div class="flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                  </svg>
                  {{ project.collaborators?.length || 1 }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredProjects.length === 0" class="text-center py-12">
          <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No projects found</h3>
          <p class="text-gray-600 mb-4">
            {{ searchQuery || statusFilter ? 'Try adjusting your search or filters.' : 'Get started by creating your first project.' }}
          </p>
          <BaseButton variant="primary" @click="createNewProject">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Create New Project
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Project Menu Dropdown -->
    <Teleport to="body">
      <div 
        v-if="showMenu && selectedProject"
        class="fixed w-48 bg-white rounded-md shadow-lg border border-gray-200 z-50"
        :style="menuStyle"
      >
        <div class="py-1">
          <button 
            @click="editProject(selectedProject); closeMenu()"
            class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
            Edit Project
          </button>
          <button 
            @click="duplicateProject(selectedProject); closeMenu()"
            class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
            Duplicate
          </button>
          <button 
            @click="exportProject(selectedProject); closeMenu()"
            class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
            Export
          </button>
          <div class="border-t border-gray-100 my-1"></div>
          <button 
            @click="archiveProject(selectedProject); closeMenu()"
            class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"></path>
            </svg>
            Archive
          </button>
          <button 
            @click="deleteProject(selectedProject); closeMenu()"
            class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
            Delete
          </button>
        </div>
      </div>
    </Teleport>

    <!-- Confirmation Dialog -->
    <ConfirmDialog
      :show="showDeleteConfirm"
      title="Delete Project"
      subtitle="Remove project permanently"
      message="Are you sure you want to delete this project? This action cannot be undone."
      :details="deleteConfirmDetails"
      confirm-text="Delete"
      cancel-text="Cancel"
      type="danger"
      confirm-variant="danger"
      :loading="deleting"
      @confirm="confirmDelete"
      @close="showDeleteConfirm = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '../components/ui/BaseButton.vue'
import PageHeader from '../components/ui/PageHeader.vue'
import ConfirmDialog from '../components/ui/ConfirmDialog.vue'

const router = useRouter()

// State
const searchQuery = ref('')
const statusFilter = ref('')
const sortBy = ref('updated')
const showMenu = ref(false)
const selectedProject = ref(null)
const menuStyle = ref({})
const showDeleteConfirm = ref(false)
const deleting = ref(false)
const projectToDelete = ref(null)

// Sample projects data (replace with actual API calls)
const projects = ref([
  {
    id: 1,
    title: 'Research Paper on AI Ethics',
    description: 'A comprehensive analysis of ethical considerations in artificial intelligence development and deployment.',
    status: 'active',
    progress: 75,
    wordCount: 8500,
    referenceCount: 12,
    createdAt: '2024-01-15T10:00:00Z',
    updatedAt: '2024-01-20T14:30:00Z',
    collaborators: [{ id: 1, name: 'John Doe' }]
  },
  {
    id: 2,
    title: 'Machine Learning Implementation Guide',
    description: 'Step-by-step guide for implementing machine learning algorithms in production environments.',
    status: 'in-progress',
    progress: 45,
    wordCount: 3200,
    referenceCount: 8,
    createdAt: '2024-01-10T09:00:00Z',
    updatedAt: '2024-01-19T16:45:00Z',
    collaborators: []
  },
  {
    id: 3,
    title: 'Data Analysis Report',
    description: 'Analysis of customer behavior patterns and market trends for Q4 2023.',
    status: 'completed',
    progress: 100,
    wordCount: 12000,
    referenceCount: 15,
    createdAt: '2023-12-01T08:00:00Z',
    updatedAt: '2023-12-28T17:20:00Z',
    collaborators: [{ id: 1, name: 'John Doe' }, { id: 2, name: 'Jane Smith' }]
  },
  {
    id: 4,
    title: 'Technical Documentation',
    description: 'Comprehensive documentation for the new API endpoints and system architecture.',
    status: 'active',
    progress: 30,
    wordCount: 1800,
    referenceCount: 5,
    createdAt: '2024-01-18T11:30:00Z',
    updatedAt: '2024-01-21T10:15:00Z',
    collaborators: []
  }
])

// Computed properties
const filteredProjects = computed(() => {
  let filtered = projects.value

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(project => 
      project.title.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query)
    )
  }

  // Apply status filter
  if (statusFilter.value) {
    filtered = filtered.filter(project => project.status === statusFilter.value)
  }

  // Apply sorting
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.title.localeCompare(b.title)
      case 'status':
        return a.status.localeCompare(b.status)
      case 'created':
        return new Date(b.createdAt) - new Date(a.createdAt)
      case 'updated':
      default:
        return new Date(b.updatedAt) - new Date(a.updatedAt)
    }
  })

  return filtered
})

const totalProjects = computed(() => projects.value.length)
const activeProjects = computed(() => projects.value.filter(p => p.status === 'active').length)
const inProgressProjects = computed(() => projects.value.filter(p => p.status === 'in-progress').length)
const completedProjects = computed(() => projects.value.filter(p => p.status === 'completed').length)

const deleteConfirmDetails = computed(() => {
  if (!projectToDelete.value) return ''
  return `This will permanently delete "${projectToDelete.value.title}" and all its associated data.`
})

// Methods
function createNewProject() {
  router.push('/project/new')
}

function openProject(project) {
  router.push(`/project/${project.id}`)
}

function showProjectMenu(project, event) {
  event.stopPropagation()
  selectedProject.value = project
  showMenu.value = true
  
  // Calculate menu position
  nextTick(() => {
    const rect = event.target.getBoundingClientRect()
    const viewportHeight = window.innerHeight
    const viewportWidth = window.innerWidth
    const menuHeight = 200 // approximate height
    const menuWidth = 192 // w-48
    
    let top = rect.bottom + 4
    let left = rect.right - menuWidth
    
    if (top + menuHeight > viewportHeight) {
      top = rect.top - menuHeight - 4
    }
    
    if (left < 0) {
      left = 4
    }
    
    if (left + menuWidth > viewportWidth) {
      left = viewportWidth - menuWidth - 4
    }
    
    menuStyle.value = {
      top: `${top}px`,
      left: `${left}px`
    }
  })
}

function closeMenu() {
  showMenu.value = false
  selectedProject.value = null
  menuStyle.value = {}
}

function editProject(project) {
  router.push(`/project/${project.id}/edit`)
}

function duplicateProject(project) {
  // Implementation for duplicating project
  console.log('Duplicate project:', project)
}

function exportProject(project) {
  // Implementation for exporting project
  console.log('Export project:', project)
}

function archiveProject(project) {
  // Implementation for archiving project
  console.log('Archive project:', project)
}

function deleteProject(project) {
  projectToDelete.value = project
  showDeleteConfirm.value = true
}

async function confirmDelete() {
  if (!projectToDelete.value) return
  
  deleting.value = true
  try {
    // Remove from local array (replace with actual API call)
    const index = projects.value.findIndex(p => p.id === projectToDelete.value.id)
    if (index > -1) {
      projects.value.splice(index, 1)
    }
    
    // Reset state
    projectToDelete.value = null
    showDeleteConfirm.value = false
  } catch (error) {
    console.error('Error deleting project:', error)
    alert('Failed to delete project. Please try again.')
  } finally {
    deleting.value = false
  }
}

function getStatusClasses(status) {
  const classes = {
    'active': 'bg-green-100 text-green-800',
    'in-progress': 'bg-yellow-100 text-yellow-800',
    'completed': 'bg-blue-100 text-blue-800',
    'archived': 'bg-gray-100 text-gray-800'
  }
  return classes[status] || classes['active']
}

function getStatusLabel(status) {
  const labels = {
    'active': 'Active',
    'in-progress': 'In Progress',
    'completed': 'Completed',
    'archived': 'Archived'
  }
  return labels[status] || 'Active'
}

function formatDate(dateString) {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) {
    return 'Today'
  } else if (diffDays === 2) {
    return 'Yesterday'
  } else if (diffDays <= 7) {
    return `${diffDays - 1} days ago`
  } else {
    return date.toLocaleDateString()
  }
}

// Click outside handler
function handleClickOutside(event) {
  if (showMenu.value && !event.target.closest('.fixed')) {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 