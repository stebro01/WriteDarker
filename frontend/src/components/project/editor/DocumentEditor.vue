<template>
  <DocumentListEditor 
    :project-id="projectId"
  />
</template>

<script setup>
import DocumentListEditor from './DocumentListEditor.vue'

// Props
defineProps({
  projectId: {
    type: Number,
    required: true
  }
})
</script>