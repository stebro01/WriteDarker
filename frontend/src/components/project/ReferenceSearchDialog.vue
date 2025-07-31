<template>
  <BaseModal
    :show="props.show"
    @close="emit('close')"
    title="Add Reference"
    size="lg"
  >
    <div class="space-y-4">
      <div class="flex space-x-2">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search references..."
          class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          @keyup.enter="performSearch"
        />
        <BaseButton @click="performSearch" :loading="searching">Search</BaseButton>
      </div>

      <div v-if="searchResults.length" class="max-h-64 overflow-y-auto border rounded">
        <ul>
          <li
            v-for="ref in searchResults"
            :key="ref.id"
            class="flex items-center justify-between p-2 border-b last:border-b-0"
          >
            <div class="pr-2">
              <div class="text-sm font-medium text-gray-800 truncate">
                {{ ref.title || ref.filename }}
              </div>
              <div class="text-xs text-gray-500">
                {{ ref.authors }}
                <span v-if="ref.year">• {{ ref.year }}</span>
              </div>
            </div>
            <BaseButton
              size="sm"
              variant="outline"
              @click="selectReference(ref)"
            >
              Add
            </BaseButton>
          </li>
        </ul>
      </div>

      <div v-else-if="hasSearched" class="text-sm text-gray-500">
        No references found.
      </div>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref } from 'vue'
import BaseModal from '../ui/BaseModal.vue'
import BaseButton from '../ui/BaseButton.vue'
import { useReferenceStore } from '../../stores/reference'
import { useApiStore } from '../../stores/api'
import { useUserStore } from '../../stores/user'

const props = defineProps({
  show: { type: Boolean, default: false },
  projectId: { type: Number, required: true }
})

const emit = defineEmits(['close', 'added'])

const referenceStore = useReferenceStore()
const apiStore = useApiStore()
const userStore = useUserStore()

const searchQuery = ref('')
const searchResults = ref([])
const hasSearched = ref(false)
const searching = ref(false)

async function performSearch() {
  if (!searchQuery.value.trim()) return
  searching.value = true
  const prev = [...referenceStore.references]
  try {
    const results = await referenceStore.fetchAll(null, { search: searchQuery.value.trim() })
    searchResults.value = results || []
  } finally {
    referenceStore.references = prev
    searching.value = false
    hasSearched.value = true
  }
}

async function selectReference(ref) {
  if (!ref?.id) return
  await apiStore.post(`/references/${ref.id}/projects/${props.projectId}?token=${userStore.token}`)
  emit('added', ref)
  emit('close')
}
</script>

