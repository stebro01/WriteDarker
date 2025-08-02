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
        Media Files ({{ media.length }})
      </q-item-section>
    </template>

    <div class="q-pa-none" style="max-height: 128px; overflow-y: auto; overflow-x: hidden; width: 100%; box-sizing: border-box;">
      <q-list dense class="q-pa-none" style="width: 100%; box-sizing: border-box;">
        <q-item
          v-for="item in media"
          :key="item.id"
          dense
          class="q-pa-xs rounded hover:bg-grey-2"
          style="min-width: 0; width: 100%; max-width: 100%; box-sizing: border-box;"
        >
          <q-item-section avatar class="min-width-auto q-pr-xs" style="flex: 0 0 auto;">
            <q-icon name="image" size="14px" color="blue-5" />
          </q-item-section>
          <q-item-section 
            clickable
            class="cursor-pointer"
            style="flex: 1 1 0; min-width: 0;"
            @click="openMediaInWindow(item)"
          >
            <q-item-label 
              class="text-caption text-weight-medium text-grey-9" 
              lines="1"
              style="word-break: break-all; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
            >
              {{ item.filename || item.label }}
            </q-item-label>
            <q-item-label 
              caption 
              class="text-grey-6"
              style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
            >
              {{ item.filetype || 'Unknown' }} • {{ formatFileSize(item.filesize) }}
            </q-item-label>
          </q-item-section>
          <q-item-section side class="min-width-auto flex items-center" style="flex: 0 0 auto;">
            <q-btn
              flat
              round
              dense
              size="xs"
              color="blue-6"
              icon="edit"
              @click.stop="editMedia(item)"
              class="q-mr-xs"
            >
              <q-tooltip class="text-caption">Edit media file</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              dense
              size="xs"
              color="red-6"
              icon="delete"
              @click.stop="deleteMedia(item)"
            >
              <q-tooltip class="text-caption">Delete media file</q-tooltip>
            </q-btn>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
    </q-expansion-item>

    <!-- Media Edit Dialog -->
    <MediaEditDialog
      :show="showMediaEdit"
      :media="selectedMedia"
      @close="showMediaEdit = false"
      @updated="handleMediaUpdated"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import MediaEditDialog from '../ui/MediaEditDialog.vue'
import { useMediaStore } from '../../stores/media'
import { windowManager } from '../../services/windowManager'

const props = defineProps({
  media: { type: Array, default: () => [] },
  expanded: { type: Boolean, default: true },
  projectId: { type: Number, default: null }
})

const emit = defineEmits(['update:expanded'])

// Stores
const mediaStore = useMediaStore()

// Dialog states
const showMediaEdit = ref(false)
const selectedMedia = ref(null)

const expandedModel = computed({
  get: () => props.expanded,
  set: val => emit('update:expanded', val)
})

function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  if (!bytes) return ''
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

function openMediaInWindow(media) {
  if (!media) return
  try {
    // Convert reactive media to plain object
    const plainMedia = JSON.parse(JSON.stringify(media))
    const window = windowManager.openMediaWindow(plainMedia)
    if (window) {
      console.log('Media opened in new window:', media.filename || media.label)
    } else {
      console.error('Failed to open media window')
    }
  } catch (error) {
    console.error('Error opening media in window:', error)
  }
}

function editMedia(media) {
  if (!media) return
  selectedMedia.value = media
  showMediaEdit.value = true
}

async function deleteMedia(media) {
  if (!media?.id) return
  
  // Show confirmation dialog
  const confirmed = confirm(`Are you sure you want to delete "${media.filename || media.label}"? This action cannot be undone.`)
  if (!confirmed) return
  
  console.log('Deleting media:', media.filename || media.label)
  
  try {
    const result = await mediaStore.delete(media.id)
    
    if (result.success) {
      console.log('Media deleted successfully')
      // Media is automatically removed from the store, so the UI will update
    } else {
      console.error('Failed to delete media:', result.error)
      alert(`Failed to delete media: ${result.error}`)
    }
  } catch (error) {
    console.error('Error deleting media:', error)
    alert('Failed to delete media. Please try again.')
  }
}

async function handleMediaUpdated() {
  if (props.projectId) {
    await mediaStore.fetch(props.projectId)
  }
}
</script>
