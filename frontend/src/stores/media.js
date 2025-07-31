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
        // Filter for media files only (not PDFs/references)
        const allDocuments = Array.isArray(data) ? data : []
        this.media = allDocuments.filter(doc => 
          doc.filetype && 
          (doc.filetype.includes('image/') || 
           doc.filetype.includes('audio/') || 
           doc.filetype.includes('video/') ||
           doc.filetype.startsWith('image') ||
           doc.filetype.startsWith('audio') ||
           doc.filetype.startsWith('video'))
        )
        console.log('Fetched documents:', allDocuments.length, 'Media files:', this.media.length)
        return this.media
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to load media'
        console.error('Media fetch error:', err)
        return []
      } finally {
        this.loading = false
      }
    },

    async upload({ projectId, file, label = '', description = '' }) {
      const userStore = useUserStore()
      if (!userStore.token || !projectId || !file) {
        console.error('Missing upload data:', { hasToken: !!userStore.token, projectId, hasFile: !!file })
        return { success: false, error: 'Missing data' }
      }
      
      console.log('Media upload started:', { 
        projectId, 
        fileName: file.name, 
        fileType: file.type, 
        fileSize: file.size,
        label 
      })
      
      const apiStore = useApiStore()
      const form = new FormData()
      form.append('project_id', String(projectId))
      if (label) form.append('label', label)
      if (description) form.append('description', description)
      
      // Use correct field names that the backend expects
      if (file.type.includes('pdf')) {
        form.append('pdf', file)
      } else {
        // Use 'image' field for all media files (images, audio, video)
        // The backend expects 'image' field for all non-PDF files
        form.append('image', file)
      }
      
      this.loading = true
      this.error = null
      try {
        console.log('Sending upload request to:', `/documents/?token=${userStore.token}`)
        const data = await apiStore.post(`/documents/?token=${userStore.token}`, form, userStore.token)
        console.log('Upload response:', data)
        
        // Only add to media list if it's actually a media file
        if (data.filetype && (
          data.filetype.includes('image/') || 
          data.filetype.includes('audio/') || 
          data.filetype.includes('video/') ||
          data.filetype.startsWith('image') ||
          data.filetype.startsWith('audio') ||
          data.filetype.startsWith('video')
        )) {
          this.media.push(data)
        }
        
        return { success: true, data }
      } catch (err) {
        console.error('Upload error:', err)
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
      if (!userStore.token || !id) return { success: false, error: 'Missing data' }
      const apiStore = useApiStore()
      this.loading = true
      this.error = null
      try {
        await apiStore.delete(`/documents/${id}?token=${userStore.token}`, userStore.token)
        this.media = this.media.filter(m => m.id !== id)
        return { success: true }
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Delete failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    }
  }
})
