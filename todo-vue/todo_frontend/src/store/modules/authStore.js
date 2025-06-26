import { defineStore } from 'pinia'
import { authService } from '@/services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || 'guest'
  },
  
  actions: {
    async login(credentials) {
      // 로그인 로직
    },
    
    async register(userData) {
      // 회원가입 로직
    },
    
    logout() {
      // 로그아웃 로직
    }
  }
})