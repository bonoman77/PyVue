<script setup>
import { ref } from 'vue'; 

const emit = defineEmits(['add-todo'])
const todo = ref('')
const hasError = ref(false)

const addTodo = () => {

  if(todo.value.trim() === '') {
    hasError.value = true
    return
  }

  emit('add-todo', {
    id: Date.now(),
    title: todo.value,
    completed: false
  })

  hasError.value = false
  todo.value = ''
}

</script>

<template>
    <form @submit.prevent="addTodo">
      <div class="d-flex">
        <div class="flex-grow-1 me-2">
        <input type="text" class="form-control" 
          v-model="todo"
          placeholder="Enter your todo"
        >
        </div> 
        <div>   
          <button type="submit" class="btn btn-primary">Add</button>
        </div>
      </div>
      <div class="text-danger" v-show="hasError">
        Please enter a todo   
      </div>      
    </form>
</template>

<style scoped>
</style>
