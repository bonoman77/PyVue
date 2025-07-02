
<template>
  <div class="sidebar-overlay" v-if="isOpen" @click="closeSidebar"></div>
  <aside class="sidebar" :class="{ 'sidebar-open': isOpen }">
    <div class="sidebar-header">
      <div class="user-info">
        <div class="user-avatar">
          <span v-if="isAuthenticated">{{ userInitials }}</span>
          <span v-else>?</span>
        </div>
        <div class="user-details" v-if="isAuthenticated">
          <h3 class="user-name">{{ currentUser?.userName || '사용자' }}</h3>
          <p class="user-email">{{ currentUser?.email || 'user@example.com' }}</p>
        </div>
        <div class="user-details" v-else>
          <h3 class="user-name">게스트</h3>
          <p class="user-email">로그인하세요</p>
        </div>
      </div>
      <button class="close-button" @click="closeSidebar">
        <span class="close-icon">&times;</span>
      </button>
    </div>
    
    <div class="sidebar-content">
      <nav class="sidebar-nav">
        <div class="nav-section">
          <h4 class="nav-title">메뉴</h4>
          <ul class="nav-list">
            <li class="nav-item">
              <router-link to="/" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">🏠</span>
                <span class="nav-text">홈</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/todo" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">✓</span>
                <span class="nav-text">할 일 목록</span>
              </router-link>
            </li>
          </ul>
        </div>
        
        <div class="nav-section">
          <h4 class="nav-title">카테고리</h4>
          <ul class="nav-list">
            <li class="nav-item">
              <router-link to="/todo?category=work" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">💼</span>
                <span class="nav-text">업무</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/todo?category=personal" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">👤</span>
                <span class="nav-text">개인</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/todo?category=shopping" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">🛒</span>
                <span class="nav-text">쇼핑</span>
              </router-link>
            </li>
          </ul>
        </div>
        
        <div class="nav-section">
          <h4 class="nav-title">계정</h4>
          <ul class="nav-list">
            <li class="nav-item" v-if="isAuthenticated">
              <router-link to="/profile" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">👤</span>
                <span class="nav-text">프로필</span>
              </router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <a href="#" class="nav-link" @click.prevent="handleLogout">
                <span class="nav-icon">🚪</span>
                <span class="nav-text">로그아웃</span>
              </a>
            </li>
            <li class="nav-item" v-else>
              <router-link to="/login" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">🔑</span>
                <span class="nav-text">로그인</span>
              </router-link>
            </li>
          </ul>
        </div>
        
        <div class="nav-section">
          <h4 class="nav-title">정보</h4>
          <ul class="nav-list">
            <li class="nav-item">
              <router-link to="/privacy-policy" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">🔒</span>
                <span class="nav-text">개인정보처리방침</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/terms-of-service" class="nav-link" @click="closeSidebar">
                <span class="nav-icon">📄</span>
                <span class="nav-text">이용약관</span>
              </router-link>
            </li>
          </ul>
        </div>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { computed, watch } from 'vue';
import { useAuthStore } from '@/store/modules/authStore';
import { useRouter } from 'vue-router';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:isOpen']);

const authStore = useAuthStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const currentUser = computed(() => authStore.currentUser);
const userInitials = computed(() => {
  if (currentUser.value?.userName) {
    return currentUser.value.userName.charAt(0).toUpperCase();
  }
  return '?';
});

const closeSidebar = () => {
  emit('update:isOpen', false);
};

const handleLogout = () => {
  authStore.logout();
  closeSidebar();
};

// 라우트가 변경될 때 사이드바 닫기
watch(() => router.currentRoute.value.path, () => {
  closeSidebar();
});
</script>

<style scoped>
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 998;
}

.sidebar {
  position: fixed;
  top: 0;
  left: -300px;
  width: 300px;
  height: 100vh;
  background-color: #ffffff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 999;
  transition: left 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.sidebar-open {
  left: 0;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #4f46e5;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 1rem;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.user-email {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  color: #6b7280;
}

.close-icon {
  display: block;
  line-height: 1;
}

.sidebar-content {
  flex: 1;
  padding: 1.5rem;
}

.nav-section {
  margin-bottom: 2rem;
}

.nav-title {
  margin: 0 0 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-radius: 0.375rem;
  color: #4b5563;
  text-decoration: none;
  transition: background-color 0.2s, color 0.2s;
}

.nav-link:hover {
  background-color: #f3f4f6;
  color: #4f46e5;
}

.router-link-active {
  background-color: #f3f4f6;
  color: #4f46e5;
  font-weight: 500;
}

.nav-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
  width: 1.5rem;
  text-align: center;
}

@media (max-width: 768px) {
  .sidebar {
    width: 280px;
    left: -280px;
  }
}
</style>