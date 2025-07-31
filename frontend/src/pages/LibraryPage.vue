<template>
  <div class="h-screen bg-gray-50 flex flex-col overflow-hidden">
    <!-- Header -->
    <PageHeader 
      title="Reference Library" 
      :show-back-button="true"
      back-route="/dashboard"
    >
      <template #actions>
        <BaseButton variant="secondary" size="sm" @click="showUpload = true">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
          Upload
        </BaseButton>
      </template>
    </PageHeader>

    <!-- Main content -->
    <div class="flex-1 overflow-auto p-6">
      <div class="max-w-5xl mx-auto">
        <div class="mb-4">
          <input v-model="filter" type="text" placeholder="Filter references..." class="border rounded p-2 w-full" />
        </div>
    <table class="min-w-full bg-white rounded-lg overflow-hidden shadow">
      <thead class="bg-gray-50 text-left">
        <tr>
          <th class="p-2 cursor-pointer" @click="sort('title')">Title</th>
          <th class="p-2 cursor-pointer" @click="sort('filename')">Filename</th>
          <th class="p-2 cursor-pointer" @click="sort('year')">Year</th>
          <th class="p-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ref in filtered" :key="ref.id" class="border-t hover:bg-gray-50">
          <td class="p-2">
            <button
              @click="previewReference(ref)"
              class="text-left hover:text-blue-600 transition-colors"
              :class="{ 'text-blue-600 cursor-pointer': canPreview(ref), 'cursor-default': !canPreview(ref) }"
            >
              {{ ref.title }}
            </button>
          </td>
          <td class="p-2 text-sm text-gray-600">
            <div class="flex items-center">
              <span class="mr-2">{{ ref.filename || 'No file' }}</span>
              <span v-if="canPreview(ref)" class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
                Preview
              </span>
            </div>
          </td>
          <td class="p-2">{{ ref.year }}</td>
          <td class="p-2">
            <div class="flex space-x-2">
              <BaseButton 
                v-if="canPreview(ref)"
                variant="outline" 
                size="sm" 
                @click="previewReference(ref)"
              >
                Preview
              </BaseButton>
              <BaseButton variant="danger" size="sm" @click="remove(ref)">Delete</BaseButton>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    
        <!-- No references message -->
        <div v-if="filtered.length === 0 && !referenceStore.loading" class="text-center py-12">
          <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="text-gray-600 mb-2">No references found</p>
          <p class="text-sm text-gray-500">Upload some files to get started</p>
        </div>
      </div>
    </div>
    
    <FileUpload :show="showUpload" @close="showUpload = false" @files-selected="uploadFiles" />
    <FilePreview :show="showPreview" :reference="selectedReference" @close="closePreview" />
    
    <!-- Confirmation Dialog -->
    <ConfirmDialog
      :show="showDeleteConfirm"
      title="Delete Reference"
      subtitle="Remove from library"
      message="Are you sure you want to delete this reference?"
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
import { ref, computed, onMounted } from 'vue'
import { useReferenceStore } from '../stores/reference'
import BaseButton from '../components/ui/BaseButton.vue'
import FileUpload from '../components/ui/FileUpload.vue'
import FilePreview from '../components/ui/FilePreview.vue'
import PageHeader from '../components/ui/PageHeader.vue'
import ConfirmDialog from '../components/ui/ConfirmDialog.vue'

const referenceStore = useReferenceStore()
const showUpload = ref(false)
const showPreview = ref(false)
const selectedReference = ref(null)
const filter = ref('')
const sortKey = ref('title')
const sortAsc = ref(true)

// Delete confirmation state
const showDeleteConfirm = ref(false)
const deleting = ref(false)
const referenceToDelete = ref(null)
const deleteConfirmDetails = computed(() => {
  if (!referenceToDelete.value) return ''
  return `This will remove "${referenceToDelete.value.title}" from your library. If other users have access to this reference, it will only be removed from your access.`
})

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

function remove(reference) {
  referenceToDelete.value = reference
  showDeleteConfirm.value = true
}

async function confirmDelete() {
  if (!referenceToDelete.value) return
  
  deleting.value = true
  try {
    await referenceStore.delete(referenceToDelete.value.id)
    // Reset state
    referenceToDelete.value = null
    showDeleteConfirm.value = false
  } catch (error) {
    console.error('Error deleting reference:', error)
    alert('Failed to delete reference. Please try again.')
  } finally {
    deleting.value = false
  }
}

function canPreview(reference) {
  if (!reference.filename) return false
  
  const filename = reference.filename.toLowerCase()
  const filetype = (reference.filetype || '').toLowerCase()
  
  // Check for supported file types
  return (
    // PDFs
    filetype.includes('pdf') || filename.endsWith('.pdf') ||
    // Images
    filetype.includes('image') || filename.endsWith('.png') || filename.endsWith('.jpg') || 
    filename.endsWith('.jpeg') || filename.endsWith('.gif') || filename.endsWith('.webp') ||
    // Text files
    filetype.includes('text') || filetype.includes('plain') || filename.endsWith('.txt') || 
    filename.endsWith('.dat') || filename.endsWith('.json')
  )
}

function previewReference(reference) {
  if (canPreview(reference)) {
    selectedReference.value = reference
    showPreview.value = true
  }
}

function closePreview() {
  showPreview.value = false
  selectedReference.value = null
}

async function uploadFiles(files) {
    for (const file of files) {
      const result = await referenceStore.upload({ query: file.name, file })
      if (!result.success) {
        if (result.isDuplicate) {
          // Show user-friendly duplicate message
          alert(`Duplicate file: ${result.error}`)
        } else {
          console.error('Upload failed:', result.error)
          alert(`Upload failed: ${result.error}`)
        }
      }
    }
}
</script>
