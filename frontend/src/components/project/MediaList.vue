<template>
  <q-expansion-item
    v-model="expandedModel"
    dense
    expand-separator
    class="text-grey-7"
    style="min-height: 50px;"
  >
    <template #header>
      <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
        Media Files ({{ media.length }})
      </q-item-section>
    </template>

    <div class="q-pa-none" style="max-height: 128px; overflow-y: auto;">
      <q-list dense class="q-pa-none">
        <q-item
          v-for="item in media"
          :key="item.id"
          dense
          clickable
          class="q-pa-xs rounded hover:bg-grey-2 cursor-pointer"
          @click="emit('select', item)"
        >
          <q-item-section avatar class="min-width-auto q-pr-xs">
            <q-icon name="image" size="14px" color="blue-5" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-caption text-weight-medium text-grey-9" lines="1">
              {{ item.filename || item.label }}
            </q-item-label>
            <q-item-label caption class="text-grey-6">
              {{ item.filetype || 'Unknown' }} • {{ formatFileSize(item.filesize) }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-expansion-item>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  media: { type: Array, default: () => [] },
  expanded: { type: Boolean, default: true }
})

const emit = defineEmits(['update:expanded', 'select'])

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
</script>
