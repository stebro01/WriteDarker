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
            </tr>
          </tbody>
        </table>
        <div v-else class="text-center py-12">
          <p class="text-gray-600">No projects found</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageHeader from '../components/ui/PageHeader.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import { useProjectStore } from '../stores/project'

const router = useRouter()
const projectStore = useProjectStore()
const filter = ref('')

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
</script>
