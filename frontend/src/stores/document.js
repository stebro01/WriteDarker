import { defineStore } from 'pinia'
import { useApiStore } from './api'
import { useUserStore } from './user'

export const useDocumentStore = defineStore('document', {
  state: () => ({
    documents: [],
    loading: false,
    activeDocumentId: null,
  }),

  getters: {
    documentsByProject: (state) => (projectId) => {
      return state.documents
        .filter(doc => doc.project_id === projectId)
        .sort((a, b) => (a.position || 0) - (b.position || 0))
    },
    
    activeDocument: (state) => {
      return state.documents.find(doc => doc.id === state.activeDocumentId)
    },
    
    pinnedDocuments: (state) => (projectId) => {
      return state.documents
        .filter(doc => doc.project_id === projectId && (doc.position || 0) < 0)
        .sort((a, b) => (a.position || 0) - (b.position || 0))
    },
    
    unpinnedDocuments: (state) => (projectId) => {
      return state.documents
        .filter(doc => doc.project_id === projectId && (doc.position || 0) >= 0)
        .sort((a, b) => (a.position || 0) - (b.position || 0))
    }
  },

  actions: {
    async fetchByProject(projectId) {
      if (!projectId) return { success: false, error: 'No project ID provided' }
      
      const userStore = useUserStore()
      if (!userStore.token) return { success: false, error: 'Not authenticated' }
      
      const apiStore = useApiStore()
      this.loading = true
      
      try {
        const query = new URLSearchParams({ token: userStore.token }).toString()
        const data = await apiStore.get(`/documents/project/${projectId}?${query}`, userStore.token)
        
        // Update documents for this project
        this.documents = this.documents.filter(doc => doc.project_id !== projectId)
        this.documents.push(...data)
        
        return { success: true, data }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to load documents'
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    },

    async create({ projectId, label, text = '', type = 'text', position }) {
      const userStore = useUserStore()
      if (!userStore.token) return { success: false, error: 'Not authenticated' }
      
      const apiStore = useApiStore()
      this.loading = true
      
      try {
        const formData = new FormData()
        formData.append('token', userStore.token)
        formData.append('label', label)
        formData.append('text', text)
        formData.append('tag', type)
        formData.append('project_id', projectId.toString())
        
        if (position !== undefined) {
          formData.append('position', position.toString())
        }
        
        const data = await apiStore.post('/documents/', formData, userStore.token)
        
        // Add to our local state
        this.documents.push(data)
        
        return { success: true, data }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to create document'
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    },

    async update(documentId, updates) {
      const userStore = useUserStore()
      if (!userStore.token) return { success: false, error: 'Not authenticated' }
      
      const apiStore = useApiStore()
      this.loading = true
      
      try {
        const query = new URLSearchParams({ token: userStore.token }).toString()
        const data = await apiStore.put(`/documents/${documentId}?${query}`, updates, userStore.token)
        
        // Update in our local state
        const index = this.documents.findIndex(doc => doc.id === documentId)
        if (index >= 0) {
          this.documents[index] = data
        }
        
        return { success: true, data }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to update document'
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    },

    async delete(documentId) {
      const userStore = useUserStore()
      if (!userStore.token) return { success: false, error: 'Not authenticated' }
      
      const apiStore = useApiStore()
      this.loading = true
      
      try {
        const query = new URLSearchParams({ token: userStore.token }).toString()
        await apiStore.delete(`/documents/${documentId}?${query}`, userStore.token)
        
        // Remove from our local state
        this.documents = this.documents.filter(doc => doc.id !== documentId)
        
        // Clear active document if it was deleted
        if (this.activeDocumentId === documentId) {
          this.activeDocumentId = null
        }
        
        return { success: true }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to delete document'
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    },

    async reorderDocuments(projectId, documentIds) {
      const userStore = useUserStore()
      if (!userStore.token) return { success: false, error: 'Not authenticated' }
      
      const apiStore = useApiStore()
      this.loading = true
      
      try {
        const query = new URLSearchParams({ token: userStore.token }).toString()
        await apiStore.post(`/documents/project/${projectId}/reorder?${query}`, documentIds, userStore.token)
        
        // Update local state positions
        documentIds.forEach((docId, index) => {
          const docIndex = this.documents.findIndex(doc => doc.id === docId)
          if (docIndex >= 0) {
            this.documents[docIndex].position = index
          }
        })
        
        return { success: true }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to reorder documents'
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    },

    async togglePin(documentId) {
      const document = this.documents.find(doc => doc.id === documentId)
      if (!document) return { success: false, error: 'Document not found' }
      
      // Pinned documents have negative positions
      const newPosition = (document.position || 0) < 0 ? 0 : -1
      
      return await this.update(documentId, { position: newPosition })
    },

    async getRevisions(documentId) {
      const userStore = useUserStore()
      if (!userStore.token) return { success: false, error: 'Not authenticated' }
      
      const apiStore = useApiStore()
      
      try {
        const query = new URLSearchParams({ token: userStore.token }).toString()
        const data = await apiStore.get(`/documents/${documentId}/revisions?${query}`, userStore.token)
        
        return { success: true, data }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to load revisions'
        return { success: false, error: errorMessage }
      }
    },

    async restoreRevision(documentId, revisionId) {
      const userStore = useUserStore()
      if (!userStore.token) return { success: false, error: 'Not authenticated' }
      
      const apiStore = useApiStore()
      this.loading = true
      
      try {
        const query = new URLSearchParams({ token: userStore.token }).toString()
        const data = await apiStore.post(`/documents/${documentId}/restore/${revisionId}?${query}`, {}, userStore.token)
        
        // Update in our local state
        const index = this.documents.findIndex(doc => doc.id === documentId)
        if (index >= 0) {
          this.documents[index] = data
        }
        
        return { success: true, data }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to restore revision'
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    },

    setActiveDocument(documentId) {
      this.activeDocumentId = documentId
    },

    clearActiveDocument() {
      this.activeDocumentId = null
    },

    // Quick create helpers for common document types
    async createQuick(projectId, type) {
      const templates = {
        abstract: { label: 'Abstract', text: '# Abstract\n\nWrite your abstract here...' },
        introduction: { label: 'Introduction', text: '# Introduction\n\nWrite your introduction here...' },
        methods: { label: 'Methods', text: '# Methods\n\nDescribe your methodology here...' },
        results: { label: 'Results', text: '# Results\n\nPresent your results here...' },
        discussion: { label: 'Discussion', text: '# Discussion\n\nDiscuss your findings here...' },
        conclusion: { label: 'Conclusion', text: '# Conclusion\n\nSummarize your conclusions here...' },
        summary: { label: 'Summary', text: '# Summary\n\nProvide a summary here...' },
        'main-idea': { label: 'Main Idea', text: '# Main Idea\n\nOutline the main idea here...' }
      }
      
      const template = templates[type] || { label: 'New Document', text: '# New Document\n\nStart writing here...' }
      
      return await this.create({
        projectId,
        ...template,
        type: 'markdown'
      })
    }
  }
})