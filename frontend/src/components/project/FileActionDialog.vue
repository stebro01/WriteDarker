<template>
  <BaseModal
    :show="show"
    @close="emit('close')"
    title="Add to Project"
    size="lg"
  >
    <div class="space-y-6">
      <!-- Section: Add new -->
      <div>
        <h3 class="text-sm font-medium text-gray-700 mb-2">Add new</h3>
        <div class="space-y-2">
          <BaseButton class="w-full justify-center" @click="emit('search-pubmed')">
            Add PubMed Reference
          </BaseButton>
          <BaseButton class="w-full justify-center" variant="outline" @click="emit('upload-pdf')">
            Upload PDF
          </BaseButton>
          <BaseButton class="w-full justify-center" variant="outline" @click="emit('upload-media')">
            Upload Image
          </BaseButton>
        </div>
      </div>

      <!-- Section: Available references -->
      <div>
        <h3 class="text-sm font-medium text-gray-700 mb-2">Available references</h3>
        <div v-if="topReferences.length" class="max-h-40 overflow-y-auto border rounded">
          <ul>
            <li
              v-for="ref in topReferences"
              :key="ref.id"
              class="flex items-center justify-between p-2 border-b last:border-b-0"
            >
              <div class="pr-2">
                <div class="text-sm font-medium text-gray-800 truncate">{{ ref.title || ref.filename }}</div>
                <div class="text-xs text-gray-500">{{ ref.authors }}</div>
              </div>
              <BaseButton size="sm" variant="outline" @click="addExisting(ref)">Add</BaseButton>
            </li>
          </ul>
        </div>
        <div v-else class="text-sm text-gray-500 mb-2">No references available.</div>

        <div class="flex space-x-2 mt-3">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search references..."
            class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            @keyup.enter="performSearch"
          />
          <BaseButton @click="performSearch" :loading="searching">Search</BaseButton>
        </div>

        <div v-if="searchResults.length" class="max-h-40 overflow-y-auto border rounded mt-2">
          <ul>
            <li
              v-for="ref in searchResults"
              :key="ref.id"
              class="flex items-center justify-between p-2 border-b last:border-b-0"
            >
              <div class="pr-2">
                <div class="text-sm font-medium text-gray-800 truncate">{{ ref.title || ref.filename }}</div>
                <div class="text-xs text-gray-500">{{ ref.authors }}</div>
              </div>
              <BaseButton size="sm" variant="outline" @click="addExisting(ref)">Add</BaseButton>
            </li>
          </ul>
        </div>
        <div v-else-if="hasSearched" class="text-sm text-gray-500 mt-2">No references found.</div>
      </div>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import BaseModal from '../ui/BaseModal.vue'
import BaseButton from '../ui/BaseButton.vue'
import { useReferenceStore } from '../../stores/reference'
import { useApiStore } from '../../stores/api'
import { useUserStore } from '../../stores/user'

const props = defineProps({
  show: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'upload-pdf', 'search-pubmed', 'upload-media', 'add-reference'])

const referenceStore = useReferenceStore()
const apiStore = useApiStore()
const userStore = useUserStore()

const topReferences = ref([])
const searchQuery = ref('')
const searchResults = ref([])
const hasSearched = ref(false)
const searching = ref(false)

watch(() => props.show, async (val) => {
  if (val) {
    await referenceStore.fetchAll()
    topReferences.value = referenceStore.references.slice(0, 5)
    searchQuery.value = ''
    searchResults.value = []
    hasSearched.value = false
  }
})

async function performSearch() {
  if (!searchQuery.value.trim()) return
  searching.value = true
  try {
    const query = encodeURIComponent(searchQuery.value.trim())
    const data = await apiStore.get(`/references/user?token=${userStore.token}&search=${query}`)
    searchResults.value = data || []
  } finally {
    searching.value = false
    hasSearched.value = true
  }
}

function addExisting(ref) {
  emit('add-reference', ref)
}
</script>
