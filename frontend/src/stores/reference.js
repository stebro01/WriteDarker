import { defineStore } from 'pinia'
import { useApiStore } from './api'
import { useUserStore } from './user'

export const useReferenceStore = defineStore('reference', {
  state: () => ({
    references: [],
    loading: false,
    error: null
  }),

  getters: {
    referenceCount: (state) => state.references.length,
    pdfCount: (state) => state.references.filter(r => r.filetype && r.filetype.includes('pdf')).length
  },

  actions: {
    async fetchAll(projectId = null, params = {}) {
      const userStore = useUserStore()
      if (!userStore.token) return
      const apiStore = useApiStore()
      this.loading = true
      try {
        const query = new URLSearchParams({ token: userStore.token, ...params }).toString()
        const endpoint = projectId ? `/references/project/${projectId}` : '/references/user'
        const data = await apiStore.get(`${endpoint}?${query}`, userStore.token)
        this.references = data
        return data
      } finally {
        this.loading = false
      }
    },

    async upload({ projectIds = [], query, file }) {
      const userStore = useUserStore()
      if (!userStore.token) return
      const apiStore = useApiStore()
      const form = new FormData()
      if (Array.isArray(projectIds)) {
        for (const pid of projectIds) {
          form.append('project_ids', pid)
        }
      }
      form.append('query', query)
      if (file) form.append('pdf', file)

      this.loading = true
      this.error = null
      try {
        const data = await apiStore.post(`/references/?token=${userStore.token}`, form, userStore.token)
        
        // Check if this reference is already in our list (could happen with shared references)
        const existingIndex = this.references.findIndex(r => r.id === data.id)
        if (existingIndex >= 0) {
          // Update existing reference
          this.references[existingIndex] = data
        } else {
          // Add new reference
          this.references.push(data)
        }
        
        return { success: true, data }
      } catch (error) {
        // Handle duplicate file error specifically
        if (error.response?.status === 409) {
          this.error = error.response.data.detail || 'File already exists in your library'
          return { success: false, error: this.error, isDuplicate: true }
        }
        // Re-throw other errors
        this.error = error.response?.data?.detail || error.message || 'Upload failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async update(id, referenceData) {
      const userStore = useUserStore()
      if (!userStore.token) return
      const apiStore = useApiStore()
      this.loading = true
      this.error = null
      try {
        const data = await apiStore.put(`/references/${id}?token=${userStore.token}`, referenceData, userStore.token)
        
        // Update the reference in our local store
        const index = this.references.findIndex(r => r.id === id)
        if (index >= 0) {
          this.references[index] = data
        }
        
        return { success: true, data }
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Update failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async delete(id) {
      const userStore = useUserStore()
      if (!userStore.token) return
      const apiStore = useApiStore()
      this.loading = true
      try {
        await apiStore.delete(`/references/${id}?token=${userStore.token}`, userStore.token)
        this.references = this.references.filter(r => r.id !== id)
      } finally {
        this.loading = false
      }
    }
  }
})
