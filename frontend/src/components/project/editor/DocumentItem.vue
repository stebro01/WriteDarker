<template>
  <div 
    :class="[
      'border-b border-gray-100 transition-all duration-200',
      isActive ? 'bg-blue-50 border-l-4 border-l-blue-500' : 'hover:bg-gray-50'
    ]"
    @click="handleFocus"
  >
    <!-- Document Header -->
    <div class="flex items-center justify-between p-4 pb-2">
      <div class="flex items-center space-x-3">
        <!-- Expand/Collapse Button -->
        <button
          @click.stop="toggleExpanded"
          class="p-1 rounded hover:bg-gray-200 transition-colors"
        >
          <svg 
            :class="['w-4 h-4 transition-transform', isExpanded ? 'rotate-90' : '']"
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
        
        <!-- Document Title -->
        <h3 :class="['font-medium flex items-center', isActive ? 'text-blue-900' : 'text-gray-900']">
          {{ document.label }}
          <!-- Unsaved changes indicator -->
          <span 
            v-if="hasUnsavedChanges && isEditing" 
            class="ml-2 w-2 h-2 bg-orange-500 rounded-full" 
            title="Unsaved changes - will auto-save in 3 seconds"
          ></span>
        </h3>
        
        <!-- Pin Indicator -->
        <svg 
          v-if="isPinned" 
          class="w-4 h-4 text-yellow-500" 
          fill="currentColor" 
          viewBox="0 0 20 20"
        >
          <path d="M11 17a1 1 0 102 0v-5h4a1 1 0 100-2h-4V4a1 1 0 10-2 0v6H7a1 1 0 100 2h4v5z"/>
        </svg>
      </div>
      
      <!-- Document Actions -->
      <div class="flex items-center space-x-1">
        <!-- Edit/Save Button -->
        <button
          v-if="!isEditing"
          @click.stop="$emit('edit', document.id)"
          class="p-2 rounded hover:bg-gray-200 text-gray-600 hover:text-gray-800"
          title="Edit document"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        
        <!-- Save Button (when editing) -->
        <button
          v-if="isEditing"
          @click.stop="saveChanges"
          class="p-2 rounded hover:bg-green-100 text-green-600 hover:text-green-800"
          title="Save document"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </button>
        
        <!-- Cancel Button (when editing) -->
        <button
          v-if="isEditing"
          @click.stop="cancelChanges"
          class="p-2 rounded hover:bg-red-100 text-red-600 hover:text-red-800"
          title="Cancel editing"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
        
        <!-- Pin Toggle -->
        <button
          @click.stop="$emit('toggle-pin', document.id)"
          :class="[
            'p-2 rounded hover:bg-gray-200',
            isPinned ? 'text-yellow-600' : 'text-gray-400'
          ]"
          :title="isPinned ? 'Unpin document' : 'Pin document'"
        >
          <q-icon name="push_pin" />
        </button>
        
        <!-- Delete Button -->
        <button
          @click.stop="$emit('delete', document.id)"
          class="p-2 rounded hover:bg-red-100 text-red-600 hover:text-red-800"
          title="Delete document"
        >
          <q-icon name="delete" />
        </button>
      </div>
    </div>
    
    <!-- Document Content -->
    <div v-if="isExpanded" class="px-4 pb-4">
      <!-- Edit Mode -->
      <div v-if="isEditing" class="space-y-3">
        <!-- Formatting Toolbar -->
        <div class="flex items-center space-x-2 p-2 bg-gray-50 rounded border">
          <button
            @click="insertFormat('h1')"
            class="px-2 py-1 text-sm rounded hover:bg-gray-200"
            title="Heading 1"
          >
            H1
          </button>
          <button
            @click="insertFormat('h2')"
            class="px-2 py-1 text-sm rounded hover:bg-gray-200"
            title="Heading 2"
          >
            H2
          </button>
          <button
            @click="insertFormat('h3')"
            class="px-2 py-1 text-sm rounded hover:bg-gray-200"
            title="Heading 3"
          >
            H3
          </button>
          <div class="w-px h-6 bg-gray-300"></div>
          <button
            @click="insertFormat('bold')"
            class="px-2 py-1 text-sm font-bold rounded hover:bg-gray-200"
            title="Bold"
          >
            B
          </button>
          <button
            @click="insertFormat('italic')"
            class="px-2 py-1 text-sm italic rounded hover:bg-gray-200"
            title="Italic"
          >
            I
          </button>
          <button
            @click="insertFormat('highlight')"
            class="px-2 py-1 text-sm rounded hover:bg-gray-200 bg-yellow-200"
            title="Highlight"
          >
            H
          </button>
        </div>
        
        <!-- Title Editor -->
        <input
          v-model="editForm.label"
          class="w-full text-lg font-medium border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Document title..."
          @keydown.enter.prevent="saveChanges"
          @keydown.escape.prevent="cancelChanges"
        />
        
        <!-- Content Editor -->
        <textarea
          ref="contentEditor"
          v-model="editForm.text"
          class="w-full min-h-32 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm leading-relaxed"
          placeholder="Start writing your document content..."
          @keydown.ctrl.enter.prevent="saveChanges"
          @keydown.ctrl.s.prevent="saveChanges"
          @keydown.escape.prevent="cancelChanges"
          @focus="handleFocus"
        ></textarea>
        
        <!-- Editor Help -->
        <div class="text-xs text-gray-500 flex items-center justify-between">
          <span>Ctrl+Enter or Ctrl+S to save • Escape to cancel • Markdown supported</span>
          <span v-if="hasUnsavedChanges" class="text-orange-600">
            Auto-saving in 3s...
          </span>
        </div>
      </div>
      
      <!-- View Mode -->
      <div v-else class="space-y-3">
        <!-- Rendered Content -->
        <div 
          class="prose prose-sm max-w-none prose-headings:text-gray-900 prose-p:text-gray-700"
          v-html="renderedContent"
          @click="handleFocus"
        ></div>
        
        <!-- Empty State -->
        <div v-if="!document.text || document.text.trim() === ''" class="text-gray-400 italic py-4">
          No content yet. Click edit to add content.
        </div>
      </div>
    </div>
    
    <!-- Collapsed Preview -->
    <div v-else class="px-4 pb-2">
      <p class="text-sm text-gray-600 line-clamp-2">
        {{ document.text || 'No content yet...' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onUnmounted } from 'vue'
import { marked } from 'marked'

// Props
const props = defineProps({
  document: {
    type: Object,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  },
  isEditing: {
    type: Boolean,
    default: false
  }
})

// Emits
const emits = defineEmits([
  'edit',
  'save',
  'cancel',
  'delete',
  'toggle-pin',
  'toggle-expand',
  'focus'
])

// Refs
const contentEditor = ref(null)
const isExpanded = ref(true)
const autoSaveTimeout = ref(null)
const hasUnsavedChanges = ref(false)

// Edit form
const editForm = ref({
  label: '',
  text: ''
})

// Computed
const isPinned = computed(() => (props.document.position || 0) < 0)

const renderedContent = computed(() => {
  if (!props.document.text) return ''
  
  try {
    // Configure marked for safe HTML rendering
    marked.setOptions({
      breaks: true,
      gfm: true,
      sanitize: false, // We'll handle this with a proper sanitizer in production
    })
    
    let html = marked(props.document.text)
    
    // Add yellow highlighting support
    html = html.replace(/==([^=]+)==/g, '<mark class="bg-yellow-200 px-1 rounded">$1</mark>')
    
    return html
  } catch (error) {
    console.error('Error rendering markdown:', error)
    return props.document.text
  }
})

// Methods
function handleFocus() {
  emits('focus', props.document.id)
}

function toggleExpanded() {
  isExpanded.value = !isExpanded.value
  emits('toggle-expand', props.document.id)
}

function saveChanges() {
  clearAutoSave()
  emits('save', props.document.id, {
    label: editForm.value.label,
    text: editForm.value.text
  })
}

function cancelChanges() {
  // Reset form to original values
  clearAutoSave()
  editForm.value = {
    label: props.document.label || '',
    text: props.document.text || ''
  }
  emits('cancel')
}

function insertFormat(type) {
  if (!contentEditor.value) return
  
  const textarea = contentEditor.value
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = textarea.value.substring(start, end)
  
  let replacement = ''
  let cursorOffset = 0
  
  switch (type) {
    case 'h1':
      replacement = `# ${selectedText || 'Heading 1'}`
      cursorOffset = selectedText ? 0 : replacement.length
      break
    case 'h2':
      replacement = `## ${selectedText || 'Heading 2'}`
      cursorOffset = selectedText ? 0 : replacement.length
      break
    case 'h3':
      replacement = `### ${selectedText || 'Heading 3'}`
      cursorOffset = selectedText ? 0 : replacement.length
      break
    case 'bold':
      replacement = `**${selectedText || 'bold text'}**`
      cursorOffset = selectedText ? 0 : replacement.length - 2
      break
    case 'italic':
      replacement = `*${selectedText || 'italic text'}*`
      cursorOffset = selectedText ? 0 : replacement.length - 1
      break
    case 'highlight':
      replacement = `==${selectedText || 'highlighted text'}==`
      cursorOffset = selectedText ? 0 : replacement.length - 2
      break
  }
  
  // Replace the selected text
  const newText = textarea.value.substring(0, start) + replacement + textarea.value.substring(end)
  editForm.value.text = newText
  
  // Set cursor position
  nextTick(() => {
    textarea.focus()
    const newCursorPos = start + replacement.length - cursorOffset
    textarea.setSelectionRange(newCursorPos, newCursorPos)
  })
}

// Auto-save functionality
function scheduleAutoSave() {
  if (autoSaveTimeout.value) {
    clearTimeout(autoSaveTimeout.value)
  }
  
  hasUnsavedChanges.value = true
  
  autoSaveTimeout.value = setTimeout(() => {
    if (hasUnsavedChanges.value && props.isEditing) {
      saveChanges()
    }
  }, 3000) // Auto-save after 3 seconds of inactivity
}

function clearAutoSave() {
  if (autoSaveTimeout.value) {
    clearTimeout(autoSaveTimeout.value)
    autoSaveTimeout.value = null
  }
  hasUnsavedChanges.value = false
}

// Watch for editing state changes
watch(() => props.isEditing, (isEditing) => {
  if (isEditing) {
    // Initialize form with current document data
    editForm.value = {
      label: props.document.label || '',
      text: props.document.text || ''
    }
    
    // Focus on the content editor after Vue updates the DOM
    nextTick(() => {
      if (contentEditor.value) {
        contentEditor.value.focus()
      }
    })
  } else {
    // Clear auto-save when no longer editing
    clearAutoSave()
  }
})

// Auto-expand when editing
watch(() => props.isEditing, (isEditing) => {
  if (isEditing) {
    isExpanded.value = true
  }
})

// Watch for changes in edit form to trigger auto-save
watch(() => editForm.value.text, () => {
  if (props.isEditing) {
    scheduleAutoSave()
  }
})

watch(() => editForm.value.label, () => {
  if (props.isEditing) {
    scheduleAutoSave()
  }
})

// Cleanup on unmount
onUnmounted(() => {
  clearAutoSave()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom scrollbar for textarea */
textarea::-webkit-scrollbar {
  width: 6px;
}

textarea::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Prose styling adjustments */
:deep(.prose) {
  color: inherit;
}

:deep(.prose h1),
:deep(.prose h2),
:deep(.prose h3),
:deep(.prose h4),
:deep(.prose h5),
:deep(.prose h6) {
  margin-top: 1em;
  margin-bottom: 0.5em;
}

:deep(.prose p) {
  margin-top: 0.75em;
  margin-bottom: 0.75em;
}

:deep(.prose ul),
:deep(.prose ol) {
  margin-top: 0.75em;
  margin-bottom: 0.75em;
}
</style>