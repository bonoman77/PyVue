

<script setup>
import { ref } from 'vue'; 

const props = defineProps({
  todos: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['delete-todo', 'toggle-todo'])

const deleteTodo = (index) => {
  emit('delete-todo', index)
}

const toggleTodo = (index) => {
  emit('toggle-todo', index)
}

</script>

<template>
    <div v-for="(todo,index) in todos" :key="todo.id" class="card py-1 my-1">
      <div class="card-body p-1 d-flex align-items-center justify-content-between">
        <div class="form-check ps-0">
          <input type="checkbox" class="form-check-input" :checked="todo.completed"
          @change="toggleTodo(index)"
          >
          <label class="form-check-label" :class="todo.completed ? 'todo-completed' : ''">{{ todo.title }}</label>
        </div>
        <div class="ms-auto">  
          <button type="button" class="btn btn-danger btn-sm" @click="deleteTodo(index)">Delete</button>
        </div>
      </div>
    </div>
</template>

<style scoped>
.card {
  padding-right: 3px;
}

.todo-completed {
  text-decoration: line-through;
  color: gray;
}
</style>
