<template>
  <div class="border-t border-gray-200 bg-gray-50/50 flex flex-col" :style="collapsed ? 'height: 48px;' : 'height: 200px;'">
    <!-- Chat header -->
    <div class="px-3 sm:px-4 md:px-6 py-2 sm:py-3 bg-white border-b border-gray-200 flex-shrink-0">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <div class="w-5 h-5 bg-gradient-to-r from-orange-400 to-orange-600 rounded-full flex items-center justify-center mr-2">
            <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
          </div>
          <div class="text-xs font-medium text-gray-600 uppercase tracking-wide">AI Assistant</div>
        </div>
        <button
          @click="$emit('toggle-collapse')"
          class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="collapsed ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Chat messages -->
    <div v-if="!collapsed" class="flex-1 overflow-y-auto p-2 sm:p-3 md:p-4 min-h-0">
      <div class="space-y-3">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="[
            'flex',
            message.isUser ? 'justify-end' : 'justify-start'
          ]"
        >
          <div
            :class="[
              'max-w-xs sm:max-w-sm lg:max-w-md px-3 py-2 rounded-lg',
              message.isUser
                ? 'bg-orange-500 text-white'
                : 'bg-white border border-gray-200 text-gray-900'
            ]"
          >
            <p class="text-xs">{{ message.text }}</p>
            <p class="text-xs mt-1 opacity-70">{{ message.time }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat input -->
    <div v-if="!collapsed" class="p-2 sm:p-3 md:p-4 bg-white border-t border-gray-200 flex-shrink-0">
      <div class="flex space-x-2 sm:space-x-3">
        <input
          v-model="inputText"
          @keyup.enter="handleSendMessage"
          class="flex-1 px-3 py-2 text-xs border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          placeholder="Ask AI for help..."
        />
        <BaseButton @click="handleSendMessage" variant="primary" size="sm" class="flex-shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
          </svg>
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseButton from '../../ui/BaseButton.vue'

// Props
defineProps({
  collapsed: {
    type: Boolean,
    default: false
  },
  messages: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits([
  'toggle-collapse',
  'send-message'
])

// Local state
const inputText = ref('')

// Methods
function handleSendMessage() {
  if (!inputText.value.trim()) return
  
  emit('send-message', inputText.value)
  inputText.value = ''
}
</script>