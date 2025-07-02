<!-- src/pages/auth/login.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/modules/authStore'
import Input from '@/components/ui/Input.vue'
import Button from '@/components/ui/Button.vue'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  userEmail: '',
  password: ''
})

const formErrors = ref({
  userEmail: '',
  password: ''
})

const validateForm = () => {
  let isValid = true
  formErrors.value.userEmail = ''
  formErrors.value.password = ''
  
  if (!formData.value.userEmail) {
    formErrors.value.userEmail = '이메일 계정을 입력해주세요.'
    isValid = false
  }
  
  if (!formData.value.password) {
    formErrors.value.password = '비밀번호를 입력해주세요.'
    isValid = false
  }
  
  return isValid
}

const handleLogin = async () => {
  if (!validateForm()) return
  
  const success = await authStore.login(formData.value)
  if (success) {
    router.push('/')
  }
}
</script>

<template>
  <div class="login-container">
    <div class="card">
      <div class="card-header">
        <h2>로그인</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleLogin">
          <Input
            v-model="formData.userEmail"
            label="이메일 계정"
            placeholder="이메일 계정을 입력하세요"
            :error="formErrors.userEmail"
            required
          />
          
          <Input
            v-model="formData.password"
            type="password"
            label="비밀번호"
            placeholder="비밀번호를 입력하세요"
            :error="formErrors.password"
            required
          />
          
          <div class="d-grid gap-2 mt-4">
            <Button
              type="submit"
              variant="primary"
              :loading="authStore.loading"
            >
              로그인
            </Button>
          </div>
          
          <div v-if="authStore.error" class="alert alert-danger mt-3">
            {{ authStore.error }}
          </div>
        </form>
      </div>
      <div class="card-footer text-center">
        <p>계정이 없으신가요? <router-link to="/register">회원가입</router-link></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
}
</style>