<!-- src/components/layout/Header.vue -->
<script setup>
import { computed, ref } from 'vue'
import { useAuthStore } from '@/store/modules/authStore'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'

const authStore = useAuthStore()
const router = useRouter()
const showDropdown = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)
const currentUser = computed(() => authStore.currentUser)

const handleLogout = () => {
  authStore.logout()
  showDropdown.value = false
}

const handleLogin = () => {
  router.push('/login')
}

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/">SMPW</router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse text-start" id="navbarNav">
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
            <div class="dropdown">
              <span 
                class="navbar-text me-3 dropdown-toggle" 
                @click="toggleDropdown"
                style="cursor: pointer;"
              >
                안녕하세요, {{ currentUser?.userName || '사용자' }}님!
              </span>
              <div 
                class="dropdown-menu" 
                :class="{ 'show': showDropdown }"
                style="position: absolute; min-width: 10rem;"
              >
                <Button 
                  variant="danger" 
                  size="sm" 
                  @click="handleLogout"
                  class="dropdown-item text-danger"
                  style="border: none; background: none;"
                >
                  로그아웃
                </Button>
              </div>
            </div>
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