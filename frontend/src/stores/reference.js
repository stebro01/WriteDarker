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
      try {
        const data = await apiStore.post(`/references/?token=${userStore.token}`, form, userStore.token)
        this.references.push(data)
        return data
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
