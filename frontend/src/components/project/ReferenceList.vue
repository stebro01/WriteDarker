<template>
  <div style="width: 100%; max-width: 100%; overflow: hidden; box-sizing: border-box;">
    <q-expansion-item
      v-model="expandedModel"
      dense
      expand-separator
      class="text-grey-7"
      style="min-height: 50px; width: 100%; max-width: 100%; overflow: hidden; box-sizing: border-box; flex-shrink: 1; min-width: 0;"
    >
      <template #header>
        <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
          References ({{ references.length }})
        </q-item-section>
      </template>

      <div class="q-pa-none" style="max-height: 128px; overflow-y: auto; overflow-x: hidden; width: 100%; box-sizing: border-box;">
        <q-list dense class="q-pa-none" style="width: 100%; box-sizing: border-box;">
          <q-item
            v-for="reference in references"
            :key="reference.id"
            dense
            class="q-pa-xs rounded hover:bg-grey-2"
            style="min-width: 0; width: 100%; max-width: 100%; box-sizing: border-box;"
          >
            <q-item-section avatar class="min-width-auto q-pr-xs" style="flex: 0 0 auto;">
              <q-icon name="description" size="14px" color="red-5" />
            </q-item-section>
                      <q-item-section 
            clickable
            class="cursor-pointer"
            style="flex: 1 1 0; min-width: 0;"
            @click="openReferenceInWindow(reference)"
          >
              <q-item-label 
                class="text-caption text-weight-medium text-grey-9" 
                lines="1"
                style="word-break: break-all; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
              >
                {{ reference.filename || reference.title }}
              </q-item-label>
              <q-item-label 
                caption 
                class="text-grey-6"
                style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
              >
                {{ getDisplayType(reference) }} • {{ formatFileSize(reference.filesize) }}
              </q-item-label>
            </q-item-section>
            <q-item-section side class="min-width-auto flex items-center" style="flex: 0 0 auto;">
              <q-btn
                flat
                round
                dense
                size="xs"
                color="red-6"
                icon="delete"
                @click.stop="removeReferenceFromProject(reference)"
              >
                <q-tooltip class="text-caption">Remove from project</q-tooltip>
              </q-btn>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-expansion-item>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { windowManager } from '../../services/windowManager'
import { useApiStore } from '../../stores/api'
import { useUserStore } from '../../stores/user'

const props = defineProps({
  references: { type: Array, default: () => [] },
  expanded: { type: Boolean, default: true },
  projectId: { type: Number, default: null }
})

const emit = defineEmits(['update:expanded', 'reference-removed'])

const expandedModel = computed({
  get: () => props.expanded,
  set: val => emit('update:expanded', val)
})

// Stores
const apiStore = useApiStore()
const userStore = useUserStore()

function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  if (!bytes) return ''
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

function getDisplayType(reference) {
  // Check if this is a PubMed article
  if (reference.pubmed_id) {
    return 'PubMed Article'
  }
  
  // If filetype is explicitly set to 'pubmed'
  if (reference.filetype === 'pubmed') {
    return 'PubMed Article'
  }
  
  // Return the original filetype or 'Unknown'
  return reference.filetype || 'Unknown'
}

function openReferenceInWindow(reference) {
  if (!reference) return
  try {
    // Use windowManager for consistent window handling
    const window = windowManager.openReferenceWindow(reference)
    if (window) {
      console.log('Reference opened in new window:', reference.filename || reference.title)
    } else {
      console.error('Failed to open reference window')
    }
  } catch (error) {
    console.error('Error opening reference in window:', error)
  }
}

async function removeReferenceFromProject(reference) {
  if (!reference?.id || !props.projectId) return
  
  // Show confirmation dialog
  const confirmed = confirm(`Are you sure you want to remove "${reference.filename || reference.title}" from this project? The reference will still be available in your library.`)
  if (!confirmed) return

  console.log('Removing reference from project:', reference.filename || reference.title)
  
  try {
    // Remove the project-reference link
    await apiStore.delete(`/references/${reference.id}/projects/${props.projectId}?token=${userStore.token}`)
    
    console.log('Reference removed from project successfully')
    emit('reference-removed', reference)
  } catch (error) {
    console.error('Error removing reference from project:', error)
    alert('Failed to remove reference from project. Please try again.')
  }
}
</script>
