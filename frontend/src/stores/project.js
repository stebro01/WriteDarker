import { defineStore } from 'pinia'
import { useApiStore } from './api'
import { useUserStore } from './user'

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [],
    loading: false,
  }),
  actions: {
    async fetchAll() {
      const userStore = useUserStore()
      if (!userStore.token) return
      const apiStore = useApiStore()
      this.loading = true
      try {
        const data = await apiStore.get(`/projects/?token=${userStore.token}`, userStore.token)
        this.projects = data
        return data
      } finally {
        this.loading = false
      }
    }
  }
})
