<!-- src/pages/auth/Profile.vue -->
<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '@/store/modules/authStore'
import Button from '@/components/ui/Button.vue'

const authStore = useAuthStore()
const currentUser = computed(() => authStore.currentUser)
const loading = ref(false)
const error = ref(null)
const successMessage = ref('')

// 비밀번호 변경 관련 상태
const showPasswordForm = ref(false)
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordError = ref('')

// 사용자 정보 불러오기
onMounted(async () => {
  if (authStore.isAuthenticated) {
    loading.value = true
    try {
      // 필요한 경우 여기서 사용자 정보를 다시 불러올 수 있습니다
      // await authStore.fetchUserProfile()
    } catch (err) {
      error.value = '사용자 정보를 불러오는데 실패했습니다.'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
})

// 비밀번호 변경 폼 토글
const togglePasswordForm = () => {
  showPasswordForm.value = !showPasswordForm.value
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  passwordError.value = ''
}

// 비밀번호 변경 처리
const changePassword = async () => {
  // 입력 검증
  if (!passwordForm.value.currentPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
    passwordError.value = '모든 필드를 입력해주세요.'
    return
  }
  
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = '새 비밀번호가 일치하지 않습니다.'
    return
  }
  
  loading.value = true
  passwordError.value = ''
  
  try {
    // 실제 API 호출은 authStore에 구현해야 합니다
    // await authStore.changePassword(passwordForm.value)
    successMessage.value = '비밀번호가 성공적으로 변경되었습니다.'
    showPasswordForm.value = false
  } catch (err) {
    passwordError.value = '비밀번호 변경에 실패했습니다. 현재 비밀번호를 확인해주세요.'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container py-4">
    <h2 class="mb-4">내 정보</h2>
    
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">로딩 중...</span>
      </div>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>
    
    <div v-else class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5>기본 정보</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <strong>사용자 이름:</strong> {{ currentUser?.userName || '정보 없음' }}
            </div>
            <div class="mb-3">
              <strong>이메일:</strong> {{ currentUser?.email || '정보 없음' }}
            </div>
            <div class="mb-3">
              <strong>가입일:</strong> {{ currentUser?.createdAt ? new Date(currentUser.createdAt).toLocaleDateString() : '정보 없음' }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5>보안 설정</h5>
            <Button 
              variant="outline-primary" 
              size="sm" 
              @click="togglePasswordForm"
            >
              {{ showPasswordForm ? '취소' : '비밀번호 변경' }}
            </Button>
          </div>
          <div class="card-body">
            <form v-if="showPasswordForm" @submit.prevent="changePassword">
              <div class="mb-3">
                <label for="currentPassword" class="form-label">현재 비밀번호</label>
                <input 
                  type="password" 
                  id="currentPassword" 
                  v-model="passwordForm.currentPassword" 
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="newPassword" class="form-label">새 비밀번호</label>
                <input 
                  type="password" 
                  id="newPassword" 
                  v-model="passwordForm.newPassword" 
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">새 비밀번호 확인</label>
                <input 
                  type="password" 
                  id="confirmPassword" 
                  v-model="passwordForm.confirmPassword" 
                  class="form-control"
                  required
                />
              </div>
              <div v-if="passwordError" class="alert alert-danger">
                {{ passwordError }}
              </div>
              <Button 
                type="submit" 
                variant="primary" 
                :disabled="loading"
              >
                변경하기
              </Button>
            </form>
            <div v-else>
              <p>계정 보안을 위해 정기적으로 비밀번호를 변경하는 것이 좋습니다.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  margin-bottom: 1.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
</style>
