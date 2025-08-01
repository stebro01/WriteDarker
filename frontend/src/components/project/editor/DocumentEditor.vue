<template>
  <div class="flex-1 flex flex-col p-4 sm:p-6 min-h-0">
    <div class="max-w-4xl mx-auto flex flex-col flex-1 min-h-0 w-full">
      <!-- Document title -->
      <input
        :value="title"
        @input="$emit('update:title', $event.target.value)"
        class="w-full text-sm sm:text-base font-medium text-gray-900 bg-transparent border-none outline-none mb-4 sm:mb-6 placeholder-gray-400 focus:placeholder-gray-300 flex-shrink-0"
        placeholder="Untitled Document"
      />
      
      <!-- Document content -->
      <div class="flex-1 flex flex-col min-h-0">
        <textarea
          :value="content"
          @input="$emit('update:content', $event.target.value)"
          class="w-full flex-1 min-h-32 resize-none border-none outline-none text-gray-700 placeholder-gray-400 leading-relaxed text-sm focus:placeholder-gray-300"
          placeholder="Start writing your document here..."
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
// Props
defineProps({
  title: {
    type: String,
    default: ''
  },
  content: {
    type: String,
    default: ''
  }
})

// Emits
defineEmits([
  'update:title',
  'update:content'
])
</script>

<style scoped>
textarea {
  font-family: inherit;
  line-height: 1.75;
  color: #374151;
}
</style>