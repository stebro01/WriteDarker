<template>
  <q-dialog 
    :model-value="show" 
    @update:model-value="$emit('close')"
    :persistent="!closeOnBackdrop"
    transition-show="scale"
    transition-hide="scale"
    :maximized="size === 'full'"
  >
    <q-card :style="cardStyle" style="position: relative; height: 100%;">
      <q-btn icon="close" flat round dense @click="$emit('close')" style="position: absolute; top: 20px; right: 20px;z-index: 1000;" />
      <div class="column full-height">
        <!-- Header -->
        <q-card-section v-if="$slots.header || title" class="row items-center q-pb-none" style="height: 100px;">
          <slot name="header">
            <div class="col">
              <div class="text-h6">{{ title }}</div>
              <div v-if="subtitle" class="text-caption text-grey-7">{{ subtitle }}</div>
            </div>
          </slot>
          
        </q-card-section>
        <q-separator />

        <!-- Content -->
        <q-card-section class="col" :class="contentClass" style="height: calc(100% - 100px - 50px);">
          <q-scroll-area style="height: 100%">
            <slot></slot>
          </q-scroll-area>
        </q-card-section>

        <!-- Footer -->
        <q-card-actions v-if="$slots.footer" align="right" style="height: 50px;">
          <slot name="footer"></slot>
        </q-card-actions>
      </div>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  closable: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  },
  padding: {
    type: String,
    default: 'md',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl'].includes(value)
  }
})

defineEmits(['close'])

const cardStyle = computed(() => {
  if (props.size === 'full') return {}
  
  const sizeStyles = {
    sm: { width: '400px', maxWidth: '90vw' },
    md: { width: '500px', maxWidth: '90vw' }, 
    lg: { width: '700px', maxWidth: '90vw' },
    xl: { width: '900px', maxWidth: '90vw' }
  }
  
  return sizeStyles[props.size] || sizeStyles.md
})

const contentClass = computed(() => {
  const paddingClasses = {
    none: 'q-pa-none',
    sm: 'q-pa-sm',
    md: 'q-pa-md', 
    lg: 'q-pa-lg',
    xl: 'q-pa-xl'
  }
  
  return paddingClasses[props.padding]
})
</script>