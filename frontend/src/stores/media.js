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
      try {
        const data = await apiStore.get(`/documents/project/${projectId}?token=${userStore.token}`, userStore.token)
        this.media = Array.isArray(data) ? data : []
        return this.media
      } finally {
        this.loading = false
      }
    },

    async upload({ projectId = null, files = [] }) {
      const userStore = useUserStore()
      if (!userStore.token || !projectId || !files.length) return
      const apiStore = useApiStore()
      this.loading = true
      this.error = null
      try {
        const uploaded = []
        for (const file of files) {
          const form = new FormData()
          form.append('project_id', projectId)
          form.append('label', file.name)
          if (file.type.includes('pdf')) {
            form.append('pdf', file)
          } else {
            form.append('image', file)
          }
          const doc = await apiStore.post(`/documents/?token=${userStore.token}`, form, userStore.token)
          uploaded.push(doc)
        }
        await this.fetch(projectId)
        return { success: true, data: uploaded }
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Upload failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async remove(id, projectId = null) {
      const userStore = useUserStore()
      if (!userStore.token) return
      const apiStore = useApiStore()
      this.loading = true
      try {
        await apiStore.delete(`/documents/${id}?token=${userStore.token}`, userStore.token)
        this.media = this.media.filter(m => m.id !== id)
        if (projectId) {
          await this.fetch(projectId)
        }
      } finally {
        this.loading = false
      }
    }
  }
})
