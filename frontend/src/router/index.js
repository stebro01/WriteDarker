import { defineRouter } from '#q-app/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from 'vue-router'
import routes from './routes'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  })

  // Global navigation guard for authentication
  Router.beforeEach(async (to, from, next) => {
    // Import user store dynamically to avoid circular dependency
    const { useUserStore } = await import('../stores/user')
    const userStore = useUserStore()
    
    // Initialize auth on first navigation if token exists
    if (!userStore.isAuthenticated && userStore.hasValidToken()) {
      try {
        await userStore.initializeAuth()
      } catch (error) {
        console.warn('Failed to initialize auth during navigation:', error)
      }
    }
    
    next()
  })

  return Router
})
