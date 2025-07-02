// src/store/modules/authStore.js
import { defineStore } from 'pinia'
import { authService } from '@/services/authService'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },
  
  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authService.login(credentials)
        this.token = response.token
        this.user = response.user
        localStorage.setItem('token', response.token)
        return true
      } catch (err) {
        this.error = err.message || '로그인에 실패했습니다.'
        console.error(err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authService.register(userData)
        this.token = response.token
        this.user = response.user
        localStorage.setItem('token', response.token)
        return true
      } catch (err) {
        this.error = err.message || '회원가입에 실패했습니다.'
        console.error(err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    async logout() {
      try {
        await authService.logout()
      } catch (err) {
        console.error('로그아웃 중 오류 발생:', err)
      } finally {
        this.resetState()
        router.push('/login')
      }
    },
    
    async fetchCurrentUser() {
      if (!this.token) return null
      
      this.loading = true
      this.error = null
      
      try {
        const user = await authService.getCurrentUser()
        this.user = user
        return user
      } catch (err) {
        this.error = err.message || '사용자 정보를 불러오는 데 실패했습니다.'
        console.error(err)
        
        // 인증 오류인 경우 로그아웃 처리
        if (err.response?.status === 401) {
          this.resetState()
        }
        return null
      } finally {
        this.loading = false
      }
    },
    
    resetState() {
      this.user = null
      this.token = null
      this.loading = false
      this.error = null
      localStorage.removeItem('token')
    }
  }
})