<script setup>
import { computed, ref } from 'vue'; 
import TodoForm from './components/TodoForm.vue'
import TodoList from './components/TodoList.vue'

const todos = ref([])

const addTodo = (todo) => {
  todos.value.push(todo)
}

const deleteTodo = (index) => {
  todos.value.splice(index, 1)
}

const toggleTodo = (index) => {
  todos.value[index].completed = !todos.value[index].completed
}

</script>


<template>
  <div class="container">
    <h2>To-Do List</h2>
    <TodoForm @add-todo="addTodo"/>
   
    <div v-if="todos.length === 0" class="text-center py-2">
      No todos available.
    </div>
    <TodoList :todos="todos" @delete-todo="deleteTodo" @toggle-todo="toggleTodo"/>
  </div>
</template>


<style scoped>
.todo-completed {
  text-decoration: line-through;
  color: gray;
}
</style>
