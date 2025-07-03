// auth.routes.js
export const authRoutes = [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/pages/auth/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/pages/auth/Register.vue')
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/pages/auth/Profile.vue'),
      meta: { requiresAuth: true }
    }
  ]