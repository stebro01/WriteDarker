import { defineStore } from 'pinia'

export const useMediaStore = defineStore('media', {
  state: () => ({
    loading: false,
    error: null
  }),
  actions: {
    async upload({ projectId = null, files = [] }) {
      // Placeholder implementation until backend media endpoints are available
      console.warn('Media upload not implemented yet', { projectId, files })
      return { success: false, error: 'Not implemented' }
    }
  }
})
