<template>
  <div class="p-6 max-w-5xl mx-auto">
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-xl font-semibold text-gray-800">Reference Library</h1>
      <BaseButton variant="secondary" size="sm" @click="showUpload = true">Upload</BaseButton>
    </div>
    <div class="mb-4">
      <input v-model="filter" type="text" placeholder="Filter" class="border rounded p-2 w-full" />
    </div>
    <table class="min-w-full bg-white rounded-lg overflow-hidden shadow">
      <thead class="bg-gray-50 text-left">
        <tr>
          <th class="p-2 cursor-pointer" @click="sort('title')">Title</th>
          <th class="p-2 cursor-pointer" @click="sort('year')">Year</th>
          <th class="p-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ref in filtered" :key="ref.id" class="border-t">
          <td class="p-2">{{ ref.title }}</td>
          <td class="p-2">{{ ref.year }}</td>
          <td class="p-2">
            <BaseButton variant="danger" size="sm" @click="remove(ref.id)">Delete</BaseButton>
          </td>
        </tr>
      </tbody>
    </table>
    <FileUpload :show="showUpload" @close="showUpload = false" @files-selected="uploadFiles" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useReferenceStore } from '../stores/reference'
import BaseButton from '../components/ui/BaseButton.vue'
import FileUpload from '../components/ui/FileUpload.vue'

const referenceStore = useReferenceStore()
const showUpload = ref(false)
const filter = ref('')
const sortKey = ref('title')
const sortAsc = ref(true)

async function fetchRefs() {
  // fetch all references for the current user
  await referenceStore.fetchAll()
}

onMounted(fetchRefs)

const filtered = computed(() => {
  let res = referenceStore.references.filter(r => r.title.toLowerCase().includes(filter.value.toLowerCase()))
  res.sort((a, b) => {
    const va = a[sortKey.value] || ''
    const vb = b[sortKey.value] || ''
    return sortAsc.value ? va.localeCompare(vb) : vb.localeCompare(va)
  })
  return res
})

function sort(key) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = true
  }
}

function remove(id) {
  referenceStore.delete(id)
}

async function uploadFiles(files) {
    for (const file of files) {
      try {
        // upload the reference without linking to a specific project
        await referenceStore.upload({ query: file.name, file })
      } catch (err) {
        console.error('upload fail', err)
      }
    }
}
</script>
