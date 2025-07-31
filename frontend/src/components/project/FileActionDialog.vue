<template>
  <BaseModal
    :show="show"
    @close="emit('close')"
    title="Add Files"
    size="sm"
  >
    <div class="space-y-3">
      <BaseButton class="w-full justify-center" @click="emit('upload-pdf')">
        Upload PDF
      </BaseButton>
      <BaseButton
        class="w-full justify-center"
        variant="outline"
        @click="emit('search-pubmed')"
      >
        Search PubMed
      </BaseButton>
      <BaseButton
        class="w-full justify-center"
        variant="outline"
        @click="emit('upload-media')"
      >
        Upload Media Files
      </BaseButton>
    </div>
  </BaseModal>
</template>

<script setup>
import BaseModal from '../ui/BaseModal.vue'
import BaseButton from '../ui/BaseButton.vue'

defineProps({
  show: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'upload-pdf', 'search-pubmed', 'upload-media'])
</script>
