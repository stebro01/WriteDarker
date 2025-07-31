import { defineStore } from 'pinia'
import { useApiStore } from './api'
import { useUserStore } from './user'

export const useMediaStore = defineStore('media', {
  state: () => ({
    media: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetch(projectId) {
      const userStore = useUserStore()
      if (!userStore.token || !projectId) return
      const apiStore = useApiStore()
      this.loading = true
      this.error = null
      try {
        const data = await apiStore.get(`/documents/project/${projectId}?token=${userStore.token}`, userStore.token)
        this.media = Array.isArray(data) ? data : []
        return this.media
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to load media'
        return []
      } finally {
        this.loading = false
      }
    },

    async upload({ projectId, file, label = '', description = '' }) {
      const userStore = useUserStore()
      if (!userStore.token || !projectId || !file) return { success: false, error: 'Missing data' }
      const apiStore = useApiStore()
      const form = new FormData()
      form.append('project_id', projectId)
      if (label) form.append('label', label)
      if (description) form.append('description', description)
      if (file.type.includes('pdf')) {
        form.append('pdf', file)
      } else {
        form.append('image', file)
      }
      this.loading = true
      this.error = null
      try {
        const data = await apiStore.post(`/documents/?token=${userStore.token}`, form, userStore.token)
        this.media.push(data)
        return { success: true, data }
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Upload failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async update(id, { label = null, description = null }) {
      const userStore = useUserStore()
      if (!userStore.token || !id) return { success: false, error: 'Missing data' }
      const apiStore = useApiStore()
      this.loading = true
      this.error = null
      try {
        const data = await apiStore.put(`/documents/${id}?token=${userStore.token}`, { label, description }, userStore.token)
        const index = this.media.findIndex(m => m.id === id)
        if (index >= 0) {
          this.media[index] = data
        }
        return { success: true, data }
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Update failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async delete(id) {
      const userStore = useUserStore()
      if (!userStore.token || !id) return
      const apiStore = useApiStore()
      this.loading = true
      this.error = null
      try {
        await apiStore.delete(`/documents/${id}?token=${userStore.token}`, userStore.token)
        this.media = this.media.filter(m => m.id !== id)
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Delete failed'
      } finally {
        this.loading = false
      }
    }
  }
})
