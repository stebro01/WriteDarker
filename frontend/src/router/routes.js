import { authGuard, guestGuard } from './auth-guard'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/auth',
    component: () => import('pages/AuthPage.vue'),
    beforeEnter: guestGuard,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    component: () => import('pages/DashboardPage.vue'),
    beforeEnter: authGuard,
    meta: { requiresAuth: true }
  },
  {
    path: '/project/new',
    component: () => import('pages/ProjectPage.vue'),
    beforeEnter: authGuard,
    meta: { requiresAuth: true }
  },
  {
    path: '/project/:id',
    component: () => import('pages/ProjectPage.vue'),
    beforeEnter: authGuard,
    meta: { requiresAuth: true }
  },
  {
    path: '/projects',
    component: () => import('pages/DashboardPage.vue'), // For now, redirect to dashboard
    beforeEnter: authGuard,
    meta: { requiresAuth: true }
  },
  {
    path: '/library',
    component: () => import('pages/LibraryPage.vue'),
    beforeEnter: authGuard,
    meta: { requiresAuth: true }
  },
  {
    path: '/legacy',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
