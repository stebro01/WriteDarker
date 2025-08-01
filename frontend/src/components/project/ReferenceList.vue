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
        References ({{ references.length }})
      </q-item-section>
      <q-item-section side>
        <BaseButton size="sm" variant="outline" @click.stop="emit('add')">
          Add Reference
        </BaseButton>
      </q-item-section>
    </template>

    <div class="q-pa-none" style="max-height: 128px; overflow-y: auto;">
      <q-list dense class="q-pa-none">
        <q-item
          v-for="reference in references"
          :key="reference.id"
          dense
          class="q-pa-xs rounded hover:bg-grey-2"
        >
          <q-item-section avatar class="min-width-auto q-pr-xs">
            <q-icon name="description" size="14px" color="red-5" />
          </q-item-section>
          <q-item-section 
            clickable
            class="cursor-pointer"
            @click="emit('preview', reference)"
          >
            <q-item-label class="text-caption text-weight-medium text-grey-9" lines="1">
              {{ reference.filename || reference.title }}
            </q-item-label>
            <q-item-label caption class="text-grey-6">
              {{ reference.filetype || 'Unknown' }} • {{ formatFileSize(reference.filesize) }}
            </q-item-label>
          </q-item-section>
          <q-item-section side class="min-width-auto">
            <q-btn
              flat
              round
              dense
              size="xs"
              color="blue-6"
              icon="open_in_new"
              @click.stop="emit('open-in-window', reference)"
              class="q-ml-xs"
            >
              <q-tooltip class="text-caption">Open in new window</q-tooltip>
            </q-btn>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-expansion-item>
</template>

<script setup>
import { computed } from 'vue'
import BaseButton from '../ui/BaseButton.vue'

const props = defineProps({
  references: { type: Array, default: () => [] },
  expanded: { type: Boolean, default: true }
})

const emit = defineEmits(['update:expanded', 'select', 'add', 'preview', 'open-in-window'])

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
