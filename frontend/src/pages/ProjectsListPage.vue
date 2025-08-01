<template>
  <div class="h-screen bg-gray-50 flex flex-col overflow-hidden">
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

    <div class="flex-1 overflow-auto p-6">
      <div class="max-w-5xl mx-auto">
        <div class="mb-4">
          <input
            v-model="filter"
            type="text"
            placeholder="Filter projects..."
            class="border rounded p-2 w-full"
          />
        </div>

        <table class="min-w-full bg-white rounded-lg overflow-hidden shadow" v-if="filteredProjects.length">
          <thead class="bg-gray-50 text-left">
            <tr>
              <th class="p-2">Project</th>
              <th class="p-2">Documents</th>
              <th class="p-2">Words</th>
              <th class="p-2">References</th>
              <th class="p-2">Media Files</th>
              <th class="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="proj in filteredProjects"
              :key="proj.id"
              class="border-t hover:bg-gray-50"
            >
              <td class="p-2">
                <button
                  @click="openProject(proj)"
                  class="text-left text-blue-600 hover:underline"
                >
                  {{ proj.label }}
                </button>
                <div class="text-xs text-gray-500">{{ proj.description }}</div>
              </td>
              <td class="p-2 text-sm text-gray-600">{{ proj.document_count }}</td>
              <td class="p-2 text-sm text-gray-600">{{ proj.word_count }}</td>
              <td class="p-2 text-sm text-gray-600">{{ proj.reference_count }}</td>
              <td class="p-2 text-sm text-gray-600">{{ proj.media_count }}</td>
              <td class="p-2">
                <div class="flex space-x-2">
                  <BaseButton
                    variant="outline"
                    size="sm"
                    @click="editProject(proj)"
                    title="Edit project"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </BaseButton>
                  <BaseButton
                    variant="danger"
                    size="sm"
                    @click="deleteProject(proj)"
                    title="Delete project"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1-1H8a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="text-center py-12">
          <p class="text-gray-600">No projects found</p>
        </div>
      </div>
    </div>

    <!-- Edit Project Dialog -->
    <ProjectEditDialog
      :show="showEditDialog"
      :project="selectedProject"
      @close="closeEditDialog"
      @updated="handleProjectUpdated"
      @deleted="handleProjectDeleted"
    />

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      :show="showDeleteDialog"
      type="danger"
      title="Delete Project"
      subtitle="This action cannot be undone"
      :message="`Are you sure you want to delete '${selectedProject?.label}'? This will permanently remove the project and all associated data.`"
      details="All references, media files, and documents associated with this project will be deleted."
      confirm-text="Delete Project"
      cancel-text="Cancel"
      :loading="deleting"
      loading-text="Deleting..."
      confirm-variant="danger"
      @confirm="confirmDelete"
      @cancel="closeDeleteDialog"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageHeader from '../components/ui/PageHeader.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import ConfirmDialog from '../components/ui/ConfirmDialog.vue'
import ProjectEditDialog from '../components/project/ProjectEditDialog.vue'
import { useProjectStore } from '../stores/project'

const router = useRouter()
const projectStore = useProjectStore()
const filter = ref('')

// Dialog state
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const selectedProject = ref(null)
const deleting = ref(false)

onMounted(() => {
  projectStore.fetchAll()
})

const filteredProjects = computed(() => {
  const q = filter.value.toLowerCase()
  if (!q) return projectStore.projects
  return projectStore.projects.filter(p =>
    (p.label || '').toLowerCase().includes(q) ||
    (p.description || '').toLowerCase().includes(q)
  )
})

function createNewProject() {
  router.push('/project/new')
}

function openProject(proj) {
  router.push(`/project/${proj.id}`)
}

function editProject(project) {
  selectedProject.value = project
  showEditDialog.value = true
}

function closeEditDialog() {
  showEditDialog.value = false
  selectedProject.value = null
}

function deleteProject(project) {
  selectedProject.value = project
  showDeleteDialog.value = true
}

function closeDeleteDialog() {
  showDeleteDialog.value = false
  selectedProject.value = null
}

async function confirmDelete() {
  if (!selectedProject.value) return

  deleting.value = true
  
  try {
    const result = await projectStore.delete(selectedProject.value.id)
    
    if (result && result.success) {
      closeDeleteDialog()
      // Refresh the projects list
      await projectStore.fetchAll()
    } else {
      console.error('Failed to delete project:', result?.error)
    }
  } catch (err) {
    console.error('Error deleting project:', err)
  } finally {
    deleting.value = false
  }
}

function handleProjectUpdated() {
  // Refresh the projects list to show updated data
  projectStore.fetchAll()
}

function handleProjectDeleted() {
  // Refresh the projects list to show updated data
  projectStore.fetchAll()
}
</script>
