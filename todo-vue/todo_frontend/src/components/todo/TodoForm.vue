<script setup>
import { ref } from 'vue'

const emit = defineEmits(['add-todo'])

const newTodo = ref({
  title: '',
  completed: false,
  contents: ''
})

const error = ref('')

// 할 일 추가
const addTodo = () => {
  if (newTodo.value.title.trim() === '') {
    error.value = '할 일을 입력해주세요.'
    return
  }
  
  error.value = ''
  emit('add-todo', { ...newTodo.value })
  newTodo.value.title = ''
  newTodo.value.contents = ''
}
</script>

<template>
  <div class="mb-3">
    <div class="input-group">
      <input 
        type="text" 
        class="form-control" 
        v-model="newTodo.title" 
        placeholder="새 할 일 입력..."
        @keyup.enter="addTodo"
      />
      <button 
        class="btn btn-primary" 
        @click="addTodo"
      >
        추가
      </button>
    </div>
    <div v-if="error" class="text-danger mt-1">{{ error }}</div>
  </div>
</template>

<style scoped>
</style>