<script setup>
import { computed, ref } from 'vue'; 
import TodoForm from './components/TodoForm.vue'
import TodoList from './components/TodoList.vue'
import axios from 'axios'


const todos = ref([])
const error = ref('')

const getTodos = async () => {
  try {
    const res = await axios.get('http://localhost:4000/boards/todo_list')
    todos.value = res.data.todo_list
  } catch (err) {
    console.log(err)
    error.value = 'Failed to get todos' 
  }
}

getTodos()

const addTodo = async (todo) => {
  try {
    const res = await axios.post('http://localhost:4000/boards/todo_insert', {
      title: todo.title,
      completed: todo.completed,
      contents: todo.contents,
    })
    todos.value.push(res.data)
  } catch (err) {
    console.log(err)
    error.value = 'Failed to add todo' 
  }
}

const deleteTodo = async (index) => {
  error.value = ''
  try {
    const todo_id = todos.value[index].todo_id
    await axios.delete('http://localhost:4000/boards/todo_delete/' + todo_id)
    todos.value.splice(index, 1)
  } catch (err) {
    console.log(err)
    error.value = 'Failed to delete todo' 
  }
}

const toggleTodo = async (index) => {
  error.value = ''
  try {
    const todo_id = todos.value[index].todo_id
    await axios.patch('http://localhost:4000/boards/todo_toggle/' + todo_id, {
      completed: !todos.value[index].completed
    })
    todos.value[index].completed = !todos.value[index].completed
  } catch (err) {
    console.log(err)
    error.value = 'Failed to toggle todo' 
  }
}

const searchText = ref('')

const filteredTodos = computed(() => {
  if (searchText.value){
    return todos.value.filter((todo) => {
      return todo.title.toLowerCase().includes(searchText.value.toLowerCase())
    })
  }
  return todos.value
})

</script>


<template>
  <div class="container">
    <h2>To-Do List</h2>

    <input type="text" 
    class="form-control mb-2"
    v-model="searchText" 
    placeholder="Search todos...">
    <TodoForm @add-todo="addTodo"/>
    <div class="text-danger">{{ error }}</div>
    <div v-if="filteredTodos.length === 0" class="text-center py-2">
      No todos available.
    </div>
    <TodoList :todos="filteredTodos" @delete-todo="deleteTodo" @toggle-todo="toggleTodo"/>
  </div>
</template>


<style scoped>

</style>
