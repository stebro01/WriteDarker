<template>
  <div class="h-screen bg-gray-50 flex flex-col overflow-hidden">
    <!-- Header -->
    <PageHeader 
      title="Reference Library" 
      :show-back-button="true"
      back-route="/dashboard"
    >
      <template #actions>
        <BaseButton variant="outline" size="sm" @click="showPubMedSearch = true" class="mr-2">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          PubMed
        </BaseButton>
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
          <th class="p-2 cursor-pointer" @click="sort('authors')">Authors</th>
          <th class="p-2 cursor-pointer" @click="sort('journal')">Journal</th>
          <th class="p-2 cursor-pointer" @click="sort('year')">Year</th>
          <th class="p-2">Source</th>
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
              {{ truncateText(ref.title, 250) }}
            </button>
            <div v-if="ref.abstract" class="text-xs text-gray-500 mt-1">
              {{ truncateText(ref.abstract, 250) }}
            </div>
          </td>
          <td class="p-2 text-sm text-gray-600">
            {{ truncateText(ref.authors || '-', 250) }}
          </td>
          <td class="p-2 text-sm text-gray-600">
            {{ truncateText(ref.journal || '-', 250) }}
          </td>
          <td class="p-2 text-sm text-gray-600">
            {{ ref.year || '-' }}
          </td>
          <td class="p-2 text-right">
            <div class="flex flex-col space-y-1">
              <span v-if="ref.pubmed_id" class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                PubMed
              </span>
              <span v-if="ref.filename" class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                </svg>
                {{ ref.filename.split('.').pop().toUpperCase() }}
              </span>
            </div>
          </td>
          <!-- Actions -->
          <td class="p-2">
            <div class="flex space-x-2">
              <BaseButton 
                v-if="canPreview(ref)"
                variant="outline" 
                size="sm" 
                @click="previewReference(ref)"
              >
                <q-icon name="visibility" />
                <q-tooltip>View Reference</q-tooltip>
              </BaseButton>
              
              <!-- Dropdown Menu -->
              <div class="relative">
                <BaseButton 
                  variant="outline" 
                  size="sm" 
                  @click="toggleDropdown(ref.id)"
                  class="px-2"
                  :data-ref-id="ref.id"
                >
                  <q-icon name="more_vert" />
                  <q-tooltip>More Actions</q-tooltip>
                </BaseButton>
              </div>
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
    <PubMedArticlePreview :show="showPubMedPreview" :reference="selectedPubMedReference" @close="closePubMedPreview" />
    <PubMedSearch :show="showPubMedSearch" @close="showPubMedSearch = false" @import-success="handlePubMedImport" />
    <ReferenceEditForm :show="showEditForm" :reference="referenceToEdit" @close="closeEditForm" @updated="handleReferenceUpdated" />
    
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
    
    <!-- Global Dropdown (Teleported to body) -->
    <Teleport to="body">
      <div 
        v-if="openDropdown && dropdownData"
        class="fixed w-48 bg-white rounded-md shadow-lg border border-gray-200 z-50"
        :style="dropdownStyle"
      >
        <div class="py-1">
          <button 
            v-if="dropdownData.url" 
            @click="openPubMedUrl(dropdownData.url); closeDropdown()"
            class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
          >
            <q-icon name="book" class="mr-2" />
            View PubMed Article
          </button>
          <button 
            @click="editReference(dropdownData); closeDropdown()"
            class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
          >
            <q-icon name="edit" class="mr-2" />
            Edit Reference
          </button>
          <button 
            @click="remove(dropdownData); closeDropdown()"
            class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center"
          >
            <q-icon name="delete" class="mr-2" />
            Delete Reference
          </button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useReferenceStore } from '../stores/reference'
import BaseButton from '../components/ui/BaseButton.vue'
import FileUpload from '../components/ui/FileUpload.vue'
import FilePreview from '../components/ui/FilePreview.vue'
import PubMedArticlePreview from '../components/ui/PubMedArticlePreview.vue'
import PageHeader from '../components/ui/PageHeader.vue'
import ConfirmDialog from '../components/ui/ConfirmDialog.vue'
import PubMedSearch from '../components/ui/PubMedSearch.vue'
import ReferenceEditForm from '../components/ui/ReferenceEditForm.vue'

const referenceStore = useReferenceStore()
const showUpload = ref(false)
const showPreview = ref(false)
const showPubMedPreview = ref(false)
const showPubMedSearch = ref(false)
const showEditForm = ref(false)
const selectedReference = ref(null)
const selectedPubMedReference = ref(null)
const referenceToEdit = ref(null)
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

// Dropdown state
const openDropdown = ref(null)
const dropdownData = ref(null)
const dropdownStyle = ref({})

async function fetchRefs() {
  // fetch all references for the current user
  await referenceStore.fetchAll()
}

onMounted(() => {
  fetchRefs()
  // Add click outside listener
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  // Remove click outside listener
  document.removeEventListener('click', handleClickOutside)
})

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
  // If it has a filename, check if it's a supported file type
  if (reference.filename) {
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
  
  // If no filename but has PubMed ID, it can be viewed as a PubMed article
  return reference.pubmed_id ? true : false
}

function previewReference(reference) {
  if (reference.filename && canPreview(reference)) {
    // For references with files, show file preview
    selectedReference.value = reference
    showPreview.value = true
  } else if (reference.pubmed_id) {
    // For PubMed articles without files, show PubMed preview
    selectedPubMedReference.value = reference
    showPubMedPreview.value = true
  }
}

function closePreview() {
  showPreview.value = false
  selectedReference.value = null
}

function closePubMedPreview() {
  showPubMedPreview.value = false
  selectedPubMedReference.value = null
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

function handlePubMedImport() {
  // Refresh the references list to show the newly imported article
  fetchRefs()
  showPubMedSearch.value = false
}

function openPubMedUrl(url) {
  window.open(url, '_blank')
}

function truncateText(text, maxLength) {
  if (!text || text.length <= maxLength) {
    return text
  }
  return text.substring(0, maxLength) + '...'
}

function editReference(reference) {
  referenceToEdit.value = reference
  showEditForm.value = true
}

function closeEditForm() {
  showEditForm.value = false
  referenceToEdit.value = null
}

function handleReferenceUpdated(updatedReference) {
  // The store is already updated by the update method
  // This is just for any additional UI feedback if needed
  console.log('Reference updated:', updatedReference)
}

function toggleDropdown(refId) {
  if (openDropdown.value === refId) {
    closeDropdown()
  } else {
    const reference = referenceStore.references.find(r => r.id === refId)
    if (reference) {
      openDropdown.value = refId
      dropdownData.value = reference
      // Calculate position after opening
      nextTick(() => {
        calculateDropdownPosition(refId)
      })
    }
  }
}

function closeDropdown() {
  openDropdown.value = null
  dropdownData.value = null
  dropdownStyle.value = {}
}

function handleClickOutside(event) {
  // Close dropdown if clicking outside
  if (openDropdown.value && !event.target.closest('[data-ref-id]') && !event.target.closest('.fixed')) {
    closeDropdown()
  }
}

function calculateDropdownPosition(refId) {
  const button = document.querySelector(`[data-ref-id="${refId}"]`)
  if (!button) return
  
  const rect = button.getBoundingClientRect()
  const viewportHeight = window.innerHeight
  const viewportWidth = window.innerWidth
  const dropdownHeight = 120 // approximate height of dropdown
  const dropdownWidth = 192 // 48 * 4 (w-48)
  
  // Calculate position
  let top = rect.bottom + 4 // 4px gap below
  let left = rect.right - dropdownWidth // align to right edge of button
  
  // Check if dropdown goes below viewport
  if (top + dropdownHeight > viewportHeight) {
    top = rect.top - dropdownHeight - 4 // position above with 4px gap
  }
  
  // Check if dropdown goes outside left edge
  if (left < 0) {
    left = 4 // minimum 4px from left edge
  }
  
  // Check if dropdown goes outside right edge
  if (left + dropdownWidth > viewportWidth) {
    left = viewportWidth - dropdownWidth - 4 // minimum 4px from right edge
  }
  
  dropdownStyle.value = {
    top: `${top}px`,
    left: `${left}px`
  }
}


</script>
