<template>
  <div :class="cardClass">
    <div v-if="$slots.header || title" class="px-6 py-4 border-b border-gray-200">
      <slot name="header">
        <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
        <p v-if="subtitle" class="text-sm text-gray-600 mt-1">{{ subtitle }}</p>
      </slot>
    </div>
    
    <div :class="bodyClass">
      <slot></slot>
    </div>
    
    <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-200 bg-gray-50">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'bordered', 'elevated', 'glass'].includes(value)
  },
  padding: {
    type: String,
    default: 'md',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl'].includes(value)
  }
})

const cardClass = computed(() => {
  const baseClasses = ['bg-white rounded-lg overflow-hidden']
  
  const variantClasses = {
    default: '',
    bordered: 'border border-gray-200',
    elevated: 'shadow-lg border border-gray-100',
    glass: 'bg-white/80 backdrop-blur-sm border border-orange-200/50 shadow-xl'
  }
  
  return [
    ...baseClasses,
    variantClasses[props.variant]
  ].join(' ')
})

const bodyClass = computed(() => {
  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
    xl: 'p-10'
  }
  
  return paddingClasses[props.padding]
})
</script>