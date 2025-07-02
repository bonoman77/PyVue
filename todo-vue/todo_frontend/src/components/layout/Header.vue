<!-- src/components/layout/Header.vue -->
<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store/modules/authStore'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'

const authStore = useAuthStore()
const router = useRouter()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const currentUser = computed(() => authStore.currentUser)

const handleLogout = () => {
  authStore.logout()
}

const handleLogin = () => {
  router.push('/login')
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/">Todo App</router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">홈</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/todo">할 일 목록</router-link>
          </li>
        </ul>
        
        <div class="d-flex">
          <template v-if="isAuthenticated">
            <span class="navbar-text me-3">
              안녕하세요, {{ currentUser?.userName || '사용자' }}님!
            </span>
            <Button 
              variant="danger" 
              size="sm" 
              @click="handleLogout"
            >
              로그아웃
            </Button>
          </template>
          <Button 
            v-else 
            variant="primary" 
            size="sm" 
            @click="handleLogin"
          >
            로그인
          </Button>
        </div>
      </div>
    </div>
  </nav>
</template>