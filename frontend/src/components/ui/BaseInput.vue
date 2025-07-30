<template>
  <div class="space-y-1">
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700">
      {{ label }}
      <span v-if="required" class="text-orange-500 ml-1">*</span>
    </label>
    
    <div class="relative">
      <div v-if="slots.prepend" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <slot name="prepend"></slot>
      </div>
      
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :autocomplete="autocomplete"
        :class="inputClass"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />
      
      <div v-if="slots.append" class="absolute inset-y-0 right-0 pr-3 flex items-center">
        <slot name="append"></slot>
      </div>
    </div>
    
    <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
    <p v-else-if="hint" class="text-sm text-gray-500">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed, useSlots } from 'vue'

const slots = useSlots()

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  autocomplete: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

defineEmits(['update:modelValue', 'blur', 'focus'])

const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const inputClass = computed(() => {
  const baseClasses = [
    'block w-full rounded-lg border transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1'
  ]

  // Size classes
  const sizeClasses = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-5 py-3 text-lg'
  }

  // State classes
  let stateClasses = []
  if (props.error) {
    stateClasses = [
      'border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500'
    ]
  } else {
    stateClasses = [
      'border-gray-300 placeholder-gray-400 focus:ring-orange-500 focus:border-orange-500'
    ]
  }

  if (props.disabled) {
    stateClasses.push('bg-gray-50 text-gray-500 cursor-not-allowed')
  } else {
    stateClasses.push('bg-white')
  }

  // Padding adjustments for slots
  const paddingClasses = []
  if (slots.prepend) {
    paddingClasses.push('pl-10')
  }
  if (slots.append) {
    paddingClasses.push('pr-10')
  }

  return [
    ...baseClasses,
    sizeClasses[props.size],
    ...stateClasses,
    ...paddingClasses
  ].join(' ')
})
</script>