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
        const query = new URLSearchParams({ token: userStore.token }).toString()
        const data = await apiStore.get(`/projects/?${query}`, userStore.token)
        this.projects = data
        return data
      } finally {
        this.loading = false
      }
    },

    async create({ label, description = '', coauthors = '' }) {
      const userStore = useUserStore()
      if (!userStore.token) return { success: false, error: 'Not authenticated' }
      
      const apiStore = useApiStore()
      this.loading = true
      try {
        const projectData = { label, description, coauthors }
        const query = new URLSearchParams({ token: userStore.token }).toString()
        const data = await apiStore.post(`/projects/?${query}`, projectData, userStore.token)
        
        // Add the new project to our list
        this.projects.push(data)
        
        return { success: true, data }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to create project'
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    },

    async fetchById(projectId) {
      const userStore = useUserStore()
      if (!userStore.token || !projectId) return { success: false, error: 'Missing data' }
      
      const apiStore = useApiStore()
      this.loading = true
      try {
        const query = new URLSearchParams({ token: userStore.token }).toString()
        const data = await apiStore.get(`/projects/${projectId}?${query}`, userStore.token)
        
        // Update the project in our list if it exists, otherwise add it
        const existingIndex = this.projects.findIndex(p => p.id === projectId)
        if (existingIndex >= 0) {
          this.projects[existingIndex] = data
        } else {
          this.projects.push(data)
        }
        
        return { success: true, data }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to load project'
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    }
  }
})
