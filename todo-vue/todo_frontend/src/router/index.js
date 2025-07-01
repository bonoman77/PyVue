import { createRouter, createWebHistory } from 'vue-router'; 
import Home from '@/pages/home.vue'
import { todoRoutes } from './todo.routes'
import { useAuthStore } from '@/store/modules/authStore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    ...todoRoutes,
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/pages/auth/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/pages/auth/Register.vue')
    }
  ]
})

// 네비게이션 가드 설정
router.beforeEach((to, from, next) => {
  // Pinia 스토어는 setup 외부에서 사용할 때 이렇게 가져와야 합니다
  const authStore = useAuthStore()
  
  // 인증이 필요한 페이지인지 확인
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // 인증이 필요한 페이지인데 로그인하지 않은 경우
  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } 
  // 이미 로그인한 상태에서 로그인/회원가입 페이지로 이동하려는 경우
  else if ((to.path === '/login' || to.path === '/register') && authStore.isAuthenticated) {
    next('/')
  }
  else {
    next()
  }
})

export default router