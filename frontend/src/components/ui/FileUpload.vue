<template>
  <BaseModal :show="show" @close="emit('close')" title="Upload Files" size="md">
    <div class="space-y-4">
      <input
        ref="inputRef"
        type="file"
        :accept="accept"
        :multiple="multiple"
        class="block w-full text-sm text-gray-500
               file:mr-4 file:py-2 file:px-4
               file:rounded-lg file:border-0
               file:text-sm file:font-semibold
               file:bg-orange-50 file:text-orange-700
               hover:file:bg-orange-100"
        @change="handleSelection"
      />
    </div>
  </BaseModal>
</template>

<script setup>
import { ref } from 'vue'
import BaseModal from './BaseModal.vue'

defineProps({
  show: { type: Boolean, default: false },
  accept: { type: String, default: '.pdf,.txt' },
  multiple: { type: Boolean, default: true }
})

const emit = defineEmits(['close', 'files-selected'])
const inputRef = ref(null)

function handleSelection(e) {
  const files = Array.from(e.target.files)
  emit('files-selected', files)
  // reset input so same file can be selected again
  inputRef.value.value = ''
  emit('close')
}
</script>
