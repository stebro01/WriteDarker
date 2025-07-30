<template>
  <div class="h-screen bg-gray-50 flex flex-col overflow-hidden">
    <!-- Header -->
    <header class="bg-white/90 backdrop-blur-sm shadow-sm border-b border-gray-200 flex-shrink-0">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-14 min-h-[3.5rem]">
          <!-- Project info and navigation -->
          <div class="flex items-center space-x-4">
            <button
              @click="goBack"
              class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            
            <div class="flex items-center">
              <div class="w-6 h-6 bg-gradient-to-r from-orange-400 to-orange-600 rounded-md flex items-center justify-center mr-2">
                <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.828 2.828 0 114 4L9 19.5l-4.5-1L9 14.5z"></path>
                </svg>
              </div>
              <h1 class="text-sm font-medium text-gray-900">{{ projectTitle }}</h1>
            </div>
          </div>

          <!-- Header actions -->
          <div class="flex items-center space-x-2 sm:space-x-3">
            <BaseButton variant="outline" size="sm" class="hidden sm:flex">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              Export
            </BaseButton>
            <!-- Mobile export button -->
            <BaseButton variant="outline" size="sm" class="flex sm:hidden p-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
            </BaseButton>
            <BaseButton variant="primary" size="sm" class="hidden sm:flex">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              Save
            </BaseButton>
            <!-- Mobile save button -->
            <BaseButton variant="primary" size="sm" class="flex sm:hidden p-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </BaseButton>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content area -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Left Sidebar - References & Files -->
      <div 
        :class="[
          'bg-white border-r border-gray-200 flex flex-col transition-all duration-300',
          leftSidebarCollapsed ? 'w-12' : 'w-80 sm:w-72 lg:w-80'
        ]"
      >
        <!-- Sidebar header -->
        <div class="p-3 border-b border-gray-200 flex items-center justify-between">
          <div v-if="!leftSidebarCollapsed" class="text-xs font-medium text-gray-600 uppercase tracking-wide">References & Files</div>
          <button
            @click="leftSidebarCollapsed = !leftSidebarCollapsed"
            class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="leftSidebarCollapsed ? 'M9 5l7 7-7 7' : 'M15 19l-7-7 7-7'"></path>
            </svg>
          </button>
        </div>

        <!-- Sidebar content -->
        <div v-if="!leftSidebarCollapsed" class="column flex-1 overflow-y-auto p-2 sm:p-3 min-h-0 sidebar-scrollable">
          <!-- File upload area -->
          <div class="col-auto mb-2 p-2 border-2 border-dashed border-gray-300 rounded-lg hover:border-orange-300 transition-colors cursor-pointer">
            <div class="row items-center justify-center q-gutter-x-sm">
              <svg class="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              <span class="text-xs text-gray-600">Drop files or click</span>
            </div>
          </div>

          <!-- References section -->
          <div class="col mb-2">
            <button 
              @click="referencesExpanded = !referencesExpanded"
              class="w-full flex items-center justify-between text-xs font-medium text-gray-600 uppercase tracking-wide mb-1 hover:text-gray-800 transition-colors"
            >
              <span>References ({{ references.length }})</span>
              <svg class="w-3 h-3 transition-transform duration-200" :class="{ 'rotate-180': referencesExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </button>
            <div v-if="referencesExpanded" class="max-h-32 overflow-y-auto space-y-1">
              <div
                v-for="reference in references"
                :key="reference.id"
                class="p-1 sm:p-1.5 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer transition-colors"
              >
                <div class="flex items-start">
                  <svg class="w-3 h-3 text-red-500 mt-0.5 mr-1.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs font-medium text-gray-900 truncate leading-tight">{{ reference.title }}</p>
                    <p class="text-xs text-gray-500 leading-tight">{{ reference.type }} • {{ reference.pages }}p</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Media files section -->
          <div class="col mb-2">
            <button 
              @click="mediaFilesExpanded = !mediaFilesExpanded"
              class="w-full flex items-center justify-between text-xs font-medium text-gray-600 uppercase tracking-wide mb-1 hover:text-gray-800 transition-colors"
            >
              <span>Media Files ({{ mediaFiles.length }})</span>
              <svg class="w-3 h-3 transition-transform duration-200" :class="{ 'rotate-180': mediaFilesExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </button>
            <div v-if="mediaFilesExpanded" class="max-h-32 overflow-y-auto space-y-1">
              <div
                v-for="media in mediaFiles"
                :key="media.id"
                class="p-1 sm:p-1.5 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer transition-colors"
              >
                <div class="flex items-start">
                  <svg class="w-3 h-3 text-blue-500 mt-0.5 mr-1.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs font-medium text-gray-900 truncate leading-tight">{{ media.name }}</p>
                    <p class="text-xs text-gray-500 leading-tight">{{ media.type }} • {{ media.size }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Collapsed sidebar icons -->
        <div v-else class="flex-1 flex flex-col items-center py-2 sm:py-4 space-y-2 sm:space-y-3 overflow-y-auto min-h-0">
          <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </button>
          <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Center - Main Document Area -->
      <div class="flex-1 flex flex-col bg-white min-h-0">
        <!-- Document editor -->
        <div class="flex-1 flex flex-col p-4 sm:p-6 min-h-0">
          <div class="max-w-4xl mx-auto flex flex-col flex-1 min-h-0 w-full">
            <!-- Document title -->
            <input
              v-model="documentTitle"
              class="w-full text-sm sm:text-base font-medium text-gray-900 bg-transparent border-none outline-none mb-4 sm:mb-6 placeholder-gray-400 focus:placeholder-gray-300 flex-shrink-0"
              placeholder="Untitled Document"
            />
            
            <!-- Document content -->
            <div class="flex-1 flex flex-col min-h-0">
              <textarea
                v-model="documentContent"
                class="w-full flex-1 min-h-32 resize-none border-none outline-none text-gray-700 placeholder-gray-400 leading-relaxed text-sm focus:placeholder-gray-300"
                placeholder="Start writing your document here..."
              ></textarea>
            </div>
          </div>
        </div>

        <!-- AI Chat section -->
        <div class="border-t border-gray-200 bg-gray-50/50 flex flex-col" :style="chatCollapsed ? 'height: 48px;' : 'height: 200px;'">
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
                @click="chatCollapsed = !chatCollapsed"
                class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="chatCollapsed ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Chat messages -->
          <div v-if="!chatCollapsed" class="flex-1 overflow-y-auto p-2 sm:p-3 md:p-4 min-h-0">
            <div class="space-y-3">
              <div
                v-for="message in chatMessages"
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
          <div v-if="!chatCollapsed" class="p-2 sm:p-3 md:p-4 bg-white border-t border-gray-200 flex-shrink-0">
            <div class="flex space-x-2 sm:space-x-3">
              <input
                v-model="chatInput"
                @keyup.enter="sendMessage"
                class="flex-1 px-3 py-2 text-xs border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Ask AI for help..."
              />
              <BaseButton @click="sendMessage" variant="primary" size="sm" class="flex-shrink-0">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                </svg>
              </BaseButton>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Sidebar - Tools & Options -->
              <div 
          :class="[
            'bg-white border-l border-gray-200 flex flex-col transition-all duration-300',
            rightSidebarCollapsed ? 'w-12' : 'w-80 sm:w-72 lg:w-80'
          ]"
        >
        <template v-if="!rightSidebarCollapsed">
          <!-- Sidebar header -->
          <div class="p-3 border-b border-gray-200 flex items-center justify-between">
            <button
              @click="rightSidebarCollapsed = !rightSidebarCollapsed"
              class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="rightSidebarCollapsed ? 'M15 19l-7-7 7-7' : 'M9 5l7 7-7 7'"></path>
              </svg>
            </button>
            <div class="text-xs font-medium text-gray-600 uppercase tracking-wide">Tools & Options</div>
          </div>

          <!-- Sidebar content -->
          <div class="flex-1 overflow-y-auto p-3 min-h-0">
            <!-- Document stats -->
            <div class="mb-6">
              <div class="text-xs font-medium text-gray-600 uppercase tracking-wide mb-3">Document Stats</div>
              <div class="space-y-3">
                <div class="bg-gray-50 rounded-lg p-3">
                  <div class="text-center">
                    <div class="text-base font-semibold text-gray-900">{{ documentStats.words }}</div>
                    <div class="text-xs text-gray-500">Words</div>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-2">
                  <div class="bg-gray-50 rounded-lg p-2 text-center">
                    <div class="text-xs font-semibold text-gray-900">{{ documentStats.characters }}</div>
                    <div class="text-xs text-gray-500">Characters</div>
                  </div>
                  <div class="bg-gray-50 rounded-lg p-2 text-center">
                    <div class="text-xs font-semibold text-gray-900">{{ documentStats.paragraphs }}</div>
                    <div class="text-xs text-gray-500">Paragraphs</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Writing tools -->
            <div class="mb-6">
              <div class="text-xs font-medium text-gray-600 uppercase tracking-wide mb-3">Writing Tools</div>
              <div class="space-y-2">
                <BaseButton variant="outline" size="sm" full-width>
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  </svg>
                  Grammar Check
                </BaseButton>
                <BaseButton variant="outline" size="sm" full-width>
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                  Improve Writing
                </BaseButton>
                <BaseButton variant="outline" size="sm" full-width>
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                  </svg>
                  Citation Generator
                </BaseButton>
              </div>
            </div>

            <!-- Export options -->
            <div class="mb-6">
              <div class="text-xs font-medium text-gray-600 uppercase tracking-wide mb-3">Export Options</div>
              <div class="space-y-2">
                <BaseButton variant="secondary" size="sm" full-width>
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  Export as PDF
                </BaseButton>
                <BaseButton variant="outline" size="sm" full-width>
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  Export as Word
                </BaseButton>
              </div>
            </div>
          </div>
        </template>
        
        <template v-else>
          <!-- Sidebar header collapsed -->
          <div class="p-3 border-b border-gray-200 flex items-center justify-between">
            <button
              @click="rightSidebarCollapsed = !rightSidebarCollapsed"
              class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="rightSidebarCollapsed ? 'M15 19l-7-7 7-7' : 'M9 5l7 7-7 7'"></path>
              </svg>
            </button>
          </div>
          
          <!-- Collapsed sidebar icons -->
          <div class="flex-1 flex flex-col items-center py-4 space-y-3 overflow-y-auto min-h-0">
            <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H9z"></path>
              </svg>
            </button>
            <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '../components/ui/BaseButton.vue'

const router = useRouter()

// Sidebar states
const leftSidebarCollapsed = ref(false)
const rightSidebarCollapsed = ref(false)
const chatCollapsed = ref(false)
const referencesExpanded = ref(true)
const mediaFilesExpanded = ref(true)

// Project data
const projectTitle = ref('Research Paper Draft')
const documentTitle = ref('The Impact of AI on Modern Writing')
const documentContent = ref('Start writing your document here...')

// Chat functionality
const chatInput = ref('')
const chatMessages = ref([
  {
    id: 1,
    text: 'Hi! I\'m here to help you with your writing. What would you like to work on?',
    isUser: false,
    time: '2 min ago'
  },
  {
    id: 2,
    text: 'Can you help me improve this introduction?',
    isUser: true,
    time: '1 min ago'
  },
  {
    id: 3,
    text: 'Of course! I\'d be happy to help you improve your introduction. Please share the text you\'d like me to review.',
    isUser: false,
    time: '30 sec ago'
  }
])

// Sample data
const references = ref([
  { id: 1, title: 'AI and Writing Automation', type: 'PDF', pages: 25 },
  { id: 2, title: 'Modern Content Creation', type: 'PDF', pages: 18 },
  { id: 3, title: 'Digital Writing Tools Study', type: 'PDF', pages: 32 }
])

const mediaFiles = ref([
  { id: 1, name: 'research_chart.png', type: 'Image', size: '2.3 MB' },
  { id: 2, name: 'interview_audio.mp3', type: 'Audio', size: '15.7 MB' }
])

// Document stats computed property
const documentStats = computed(() => {
  const text = documentContent.value || ''
  const words = text.trim() ? text.trim().split(/\s+/).length : 0
  const characters = text.length
  const paragraphs = text.trim() ? text.split(/\n\s*\n/).length : 0
  
  return { words, characters, paragraphs }
})

// Methods
const goBack = () => {
  router.push('/dashboard')
}

const sendMessage = () => {
  if (!chatInput.value.trim()) return
  
  const newMessage = {
    id: Date.now(),
    text: chatInput.value,
    isUser: true,
    time: 'now'
  }
  
  chatMessages.value.push(newMessage)
  chatInput.value = ''
  
  // Simulate AI response
  setTimeout(() => {
    const aiResponse = {
      id: Date.now() + 1,
      text: 'I understand your question. Let me help you with that...',
      isUser: false,
      time: 'now'
    }
    chatMessages.value.push(aiResponse)
  }, 1000)
}

onMounted(() => {
  // Any initialization logic here
})
</script>

<style scoped>
.prose {
  @apply text-gray-700;
}
.prose textarea {
  font-family: inherit;
  line-height: 1.75;
}
</style>