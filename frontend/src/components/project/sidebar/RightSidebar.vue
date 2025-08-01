<template>
  <div 
    :class="[
      'bg-white border-l border-gray-200 flex flex-col transition-all duration-300',
      collapsed ? 'w-12' : 'w-80 sm:w-72 lg:w-80'
    ]"
  >
    <template v-if="!collapsed">
      <!-- Sidebar header -->
      <div class="p-3 border-b border-gray-200 flex items-center justify-between">
        <button
          @click="$emit('toggle-collapse')"
          class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="collapsed ? 'M15 19l-7-7 7-7' : 'M9 5l7 7-7 7'"></path>
          </svg>
        </button>
        <div class="text-xs font-medium text-gray-600 uppercase tracking-wide">Tools & Options</div>
      </div>

      <!-- Sidebar content -->
      <div class="flex-1 overflow-y-auto min-h-0">
        <q-list dense class="q-pa-none">
          <!-- Project Information section -->
          <q-expansion-item
            v-if="currentProject && !isNewProject"
            v-model="projectInfoExpanded" 
            dense
            expand-separator
            class="text-grey-7"
            style="min-height: 50px;"
          >
            <template v-slot:header>
              <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
                Project Information
              </q-item-section>
            </template>
            
            <div class="q-pa-sm">
              <!-- Project ID badge with edit button -->
              <div class="q-mb-sm q-pa-sm bg-blue-1 rounded">
                <div class="row items-center justify-between">
                  <div class="text-caption text-weight-bold text-blue-9">ID: {{ currentProject.id }}</div>
                  <q-btn
                    flat
                    round
                    dense
                    size="xs"
                    color="blue-7"
                    icon="edit"
                    @click="$emit('edit-project')"
                    class="q-ml-sm"
                  >
                    <q-tooltip class="text-caption">Edit Project</q-tooltip>
                  </q-btn>
                </div>
              </div>
              
              <!-- Project details -->
              <div class="column q-gutter-y-xs">
                <div class="q-pa-xs bg-grey-2 rounded">
                  <div class="text-caption text-weight-bold text-grey-9">{{ currentProject.label }}</div>
                  <div class="text-caption text-grey-6" style="font-size: 10px;">Project Name</div>
                </div>
                <div v-if="currentProject.description" class="q-pa-xs bg-grey-2 rounded">
                  <div class="text-caption text-grey-9">{{ currentProject.description }}</div>
                  <div class="text-caption text-grey-6" style="font-size: 10px;">Description</div>
                </div>
                <div v-if="currentProject.coauthors" class="q-pa-xs bg-grey-2 rounded">
                  <div class="text-caption text-grey-9">{{ currentProject.coauthors }}</div>
                  <div class="text-caption text-grey-6" style="font-size: 10px;">Co-authors</div>
                </div>
              </div>
            </div>
          </q-expansion-item>

          <!-- Document Stats section -->
          <q-expansion-item
            v-model="documentStatsExpanded" 
            dense
            expand-separator
            class="text-grey-7"
            style="min-height: 50px;"
          >
            <template v-slot:header>
              <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
                Document Stats
              </q-item-section>
            </template>
            
            <div class="q-pa-sm">
              <!-- Main word count -->
              <div class="q-mb-sm q-pa-sm bg-grey-2 rounded text-center">
                <div class="text-h6 text-weight-bold text-grey-9">{{ documentStats.words }}</div>
                <div class="text-caption text-grey-6">Words</div>
              </div>
              
              <!-- Secondary stats -->
              <div class="row q-gutter-xs">
                <div class="col q-pa-xs bg-grey-2 rounded text-center">
                  <div class="text-caption text-weight-bold text-grey-9">{{ documentStats.characters }}</div>
                  <div class="text-caption text-grey-6" style="font-size: 10px;">Characters</div>
                </div>
                <div class="col q-pa-xs bg-grey-2 rounded text-center">
                  <div class="text-caption text-weight-bold text-grey-9">{{ documentStats.paragraphs }}</div>
                  <div class="text-caption text-grey-6" style="font-size: 10px;">Paragraphs</div>
                </div>
              </div>
            </div>
          </q-expansion-item>

          <!-- Writing Tools section -->
          <q-expansion-item
            v-model="writingToolsExpanded"
            dense
            expand-separator
            class="text-grey-7"
            style="min-height: 50px;"
          >
            <template v-slot:header>
              <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
                Writing Tools
              </q-item-section>
            </template>
            
            <div class="q-pa-sm column q-gutter-y-xs">
              <q-btn 
                outline
                dense
                size="sm"
                color="grey-7"
                class="q-py-xs text-caption"
                icon="spellcheck"
                label="Grammar Check"
              />
              <q-btn 
                outline
                dense
                size="sm"
                color="grey-7"
                class="q-py-xs text-caption"
                icon="auto_fix_high"
                label="Improve Writing"
              />
              <q-btn 
                outline
                dense
                size="sm"
                color="grey-7"
                class="q-py-xs text-caption"
                icon="format_quote"
                label="Citation Generator"
              />
            </div>
          </q-expansion-item>

          <!-- Export Options section -->
          <q-expansion-item
            v-model="exportOptionsExpanded"
            dense
            expand-separator
            class="text-grey-7"
            style="min-height: 50px;"
          >
            <template v-slot:header>
              <q-item-section class="text-caption text-weight-medium text-uppercase" style="letter-spacing: 0.05em;">
                Export Options
              </q-item-section>
            </template>
            
            <div class="q-pa-sm column q-gutter-y-xs">
              <q-btn 
                unelevated
                dense
                size="sm"
                color="orange-6"
                text-color="white"
                class="q-py-xs text-caption"
                icon="picture_as_pdf"
                label="Export as PDF"
              />
              <q-btn 
                outline
                dense
                size="sm"
                color="grey-7"
                class="q-py-xs text-caption"
                icon="description"
                label="Export as Word"
              />
            </div>
          </q-expansion-item>
        </q-list>
      </div>
    </template>
        
    <template v-else>
      <!-- Sidebar header collapsed -->
      <div class="p-3 border-b border-gray-200 flex items-center justify-between">
        <button
          @click="$emit('toggle-collapse')"
          class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="collapsed ? 'M15 19l-7-7 7-7' : 'M9 5l7 7-7 7'"></path>
          </svg>
        </button>
      </div>
      
      <!-- Collapsed sidebar icons -->
      <div class="column items-center q-py-sm q-gutter-y-sm overflow-y-auto min-h-0">
        <q-btn 
          flat
          round
          dense
          size="sm"
          color="grey-6"
          icon="bar_chart"
          class="q-pa-xs"
        />
        <q-btn 
          flat
          round
          dense
          size="sm"
          color="grey-6"
          icon="edit"
          class="q-pa-xs"
        />
        <q-btn
          flat
          round
          dense
          size="sm"
          color="grey-6"
          icon="download"
          class="q-pa-xs"
        />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props
const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false
  },
  currentProject: {
    type: Object,
    default: null
  },
  isNewProject: {
    type: Boolean,
    default: false
  },
  documentContent: {
    type: String,
    default: ''
  }
})

// Emits
defineEmits([
  'toggle-collapse',
  'edit-project'
])

// Local state
const projectInfoExpanded = ref(true)
const documentStatsExpanded = ref(true)
const writingToolsExpanded = ref(true)
const exportOptionsExpanded = ref(true)

// Computed properties
const documentStats = computed(() => {
  const text = props.documentContent || ''
  const words = text.trim() ? text.trim().split(/\s+/).length : 0
  const characters = text.length
  const paragraphs = text.trim() ? text.split(/\n\s*\n/).length : 0
  
  return { words, characters, paragraphs }
})
</script>