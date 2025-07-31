import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useApiStore = defineStore('api', {
  state: () => ({
    loading: false,
    error: null,
  }),

  getters: {
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error,
  },

  actions: {
    // Create axios instance with base configuration
    createAxiosInstance(token = null) {
      const instance = axios.create({
        baseURL: API_BASE_URL,
        timeout: 10000,
      })

      // Add request interceptor for authentication
      instance.interceptors.request.use(
        (config) => {
          this.loading = true
          this.error = null
          
          // Add auth token if provided
          if (token) {
            config.headers.Authorization = `Bearer ${token}`
          }
          
          return config
        },
        (error) => {
          this.loading = false
          this.error = error.message
          return Promise.reject(error)
        }
      )

      // Add response interceptor for error handling
      instance.interceptors.response.use(
        (response) => {
          this.loading = false
          return response
        },
        (error) => {
          this.loading = false
          
          if (error.response) {
            // Server responded with error status
            this.error = error.response.data?.detail || error.response.statusText
          } else if (error.request) {
            // Request was made but no response received
            this.error = 'Network error - no response from server'
          } else {
            // Something else happened
            this.error = error.message
          }
          
          return Promise.reject(error)
        }
      )

      return instance
    },

    // Generic HTTP methods
    async get(url, token = null) {
      const api = this.createAxiosInstance(token)
      const response = await api.get(url)
      return response.data
    },

    async post(url, data = {}, token = null) {
      const api = this.createAxiosInstance(token)
      const response = await api.post(url, data)
      return response.data
    },

    async put(url, data = {}, token = null) {
      const api = this.createAxiosInstance(token)
      const response = await api.put(url, data)
      return response.data
    },

    async delete(url, token = null) {
      const api = this.createAxiosInstance(token)
      const response = await api.delete(url)
      return response.data
    },

    // Authentication specific API methods
    async register(userData) {
      return await this.post('/auth/register', userData)
    },

    async login(credentials) {
      return await this.post('/auth/login', credentials)
    },

    async getCurrentUser(token) {
      return await this.get(`/auth/me?token=${token}`, token)
    },

    async updateUser(userData, token) {
      return await this.put(`/auth/me?token=${token}`, userData, token)
    },

    async changePassword(currentPassword, newPassword, token) {
      return await this.put(`/auth/me?token=${token}`, {
        password: newPassword
      }, token)
    },

    async logout() {
      return await this.post('/auth/logout')
    },

    // Clear error state
    clearError() {
      this.error = null
    },
  },
})