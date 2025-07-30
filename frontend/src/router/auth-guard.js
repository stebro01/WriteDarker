import { useUserStore } from '../stores/user'

export const authGuard = async (to, from, next) => {
  const userStore = useUserStore()
  
  // Initialize auth state if not already done
  if (!userStore.isAuthenticated && userStore.hasValidToken()) {
    try {
      await userStore.initializeAuth()
    } catch (error) {
      console.warn('Failed to initialize auth:', error)
      // Token might be invalid, will be handled by isLoggedIn check
    }
  }
  
  if (userStore.isLoggedIn) {
    next()
  } else {
    // Redirect to auth page with return path
    next({
      path: '/auth',
      query: { redirect: to.fullPath }
    })
  }
}

export const guestGuard = (to, from, next) => {
  const userStore = useUserStore()
  
  if (userStore.isLoggedIn) {
    // If already logged in, redirect to dashboard or intended page
    const redirect = to.query.redirect || '/dashboard'
    next(redirect)
  } else {
    next()
  }
}