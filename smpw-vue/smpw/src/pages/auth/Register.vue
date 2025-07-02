<!-- src/pages/auth/register.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/modules/authStore'
import Input from '@/components/ui/Input.vue'
import Button from '@/components/ui/Button.vue'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const formErrors = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateForm = () => {
  let isValid = true
  formErrors.value.name = ''
  formErrors.value.email = ''
  formErrors.value.password = ''
  formErrors.value.confirmPassword = ''
  
  // 이름 검증
  if (!formData.value.name) {
    formErrors.value.name = '이름을 입력해주세요.'
    isValid = false
  }
  
  // 이메일 검증
  if (!formData.value.email) {
    formErrors.value.email = '이메일을 입력해주세요.'
    isValid = false
  } else if (!/\S+@\S+\.\S+/.test(formData.value.email)) {
    formErrors.value.email = '올바른 이메일 형식이 아닙니다.'
    isValid = false
  }
  
  // 비밀번호 검증
  if (!formData.value.password) {
    formErrors.value.password = '비밀번호를 입력해주세요.'
    isValid = false
  } else if (formData.value.password.length < 6) {
    formErrors.value.password = '비밀번호는 최소 6자 이상이어야 합니다.'
    isValid = false
  }
  
  // 비밀번호 확인 검증
  if (!formData.value.confirmPassword) {
    formErrors.value.confirmPassword = '비밀번호 확인을 입력해주세요.'
    isValid = false
  } else if (formData.value.password !== formData.value.confirmPassword) {
    formErrors.value.confirmPassword = '비밀번호가 일치하지 않습니다.'
    isValid = false
  }
  
  return isValid
}

const handleRegister = async () => {
  if (!validateForm()) return
  
  const userData = {
    name: formData.value.name,
    email: formData.value.email,
    password: formData.value.password
  }
  
  const success = await authStore.register(userData)
  if (success) {
    router.push('/')
  }
}
</script>

<template>
  <div class="register-container">
    <div class="card">
      <div class="card-header">
        <h2>회원가입</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleRegister">
          <Input
            v-model="formData.name"
            label="이름"
            placeholder="이름을 입력하세요"
            :error="formErrors.name"
            required
          />
          
          <Input
            v-model="formData.email"
            type="email"
            label="이메일"
            placeholder="이메일을 입력하세요"
            :error="formErrors.email"
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
          
          <Input
            v-model="formData.confirmPassword"
            type="password"
            label="비밀번호 확인"
            placeholder="비밀번호를 다시 입력하세요"
            :error="formErrors.confirmPassword"
            required
          />
          
          <div class="d-grid gap-2 mt-4">
            <Button
              type="submit"
              variant="primary"
              :loading="authStore.loading"
            >
              회원가입
            </Button>
          </div>
          
          <div v-if="authStore.error" class="alert alert-danger mt-3">
            {{ authStore.error }}
          </div>
        </form>
      </div>
      <div class="card-footer text-center">
        <p>이미 계정이 있으신가요? <router-link to="/login">로그인</router-link></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 2rem auto;
}
</style>