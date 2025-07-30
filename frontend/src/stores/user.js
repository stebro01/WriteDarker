import { defineStore } from 'pinia'
import { useApiStore } from './api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('auth_token') || null,
    isAuthenticated: false,
    loading: false,
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated && !!state.token,
    userInitials: (state) => {
      if (!state.user) return ''
      const first = state.user.first_name?.[0] || ''
      const last = state.user.last_name?.[0] || ''
      return (first + last).toUpperCase() || state.user.username?.[0]?.toUpperCase() || '?'
    },
    userDisplayName: (state) => {
      if (!state.user) return ''
      if (state.user.first_name || state.user.last_name) {
        return `${state.user.first_name || ''} ${state.user.last_name || ''}`.trim()
      }
      return state.user.username
    },
  },

  actions: {
    // Initialize user session on app start
    async initializeAuth() {
      if (this.token) {
        try {
          await this.fetchCurrentUser()
        } catch {
          // Token might be expired or invalid
          this.logout()
        }
      }
    },

    // Register new user
    async register(userData) {
      this.loading = true
      try {
        const apiStore = useApiStore()
        const newUser = await apiStore.register(userData)
        
        // Auto-login after registration
        const loginResponse = await apiStore.login({
          username: userData.username,
          password: userData.password
        })
        
        this.setAuthData(loginResponse.access_token, newUser)
        return newUser
      } finally {
        this.loading = false
      }
    },

    // Login user
    async login(credentials) {
      this.loading = true
      try {
        const apiStore = useApiStore()
        const tokenResponse = await apiStore.login(credentials)
        
        // Store token temporarily to fetch user data
        const tempToken = tokenResponse.access_token
        const userData = await apiStore.getCurrentUser(tempToken)
        
        this.setAuthData(tempToken, userData)
        return userData
      } catch (error) {
        this.logout()
        throw error
      } finally {
        this.loading = false
      }
    },

    // Fetch current user data
    async fetchCurrentUser() {
      if (!this.token) {
        throw new Error('No authentication token available')
      }

      try {
        const apiStore = useApiStore()
        const userData = await apiStore.getCurrentUser(this.token)
        this.user = userData
        this.isAuthenticated = true
        return userData
      } catch (error) {
        this.logout()
        throw error
      }
    },

    // Update user profile
    async updateProfile(updateData) {
      if (!this.token) {
        throw new Error('Not authenticated')
      }

      this.loading = true
      try {
        const apiStore = useApiStore()
        const updatedUser = await apiStore.updateUser(updateData, this.token)
        this.user = updatedUser
        return updatedUser
      } finally {
        this.loading = false
      }
    },

    // Logout user
    async logout() {
      try {
        if (this.token) {
          const apiStore = useApiStore()
          await apiStore.logout()
        }
      } catch (error) {
        // Ignore logout errors, just clear local state
        console.warn('Logout API call failed:', error)
      } finally {
        this.clearAuthData()
      }
    },

    // Set authentication data
    setAuthData(token, user) {
      this.token = token
      this.user = user
      this.isAuthenticated = true
      
      // Persist token to localStorage
      localStorage.setItem('auth_token', token)
    },

    // Clear authentication data
    clearAuthData() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      
      // Remove token from localStorage
      localStorage.removeItem('auth_token')
    },

    // Check if token exists and is valid format
    hasValidToken() {
      return !!this.token && this.token.length > 0
    },
  },
})