<script setup>
import { computed, ref } from 'vue'; 
import TodoForm from './components/TodoForm.vue'
import TodoList from './components/TodoList.vue'
import axios from 'axios'


const todos = ref([])
const error = ref('')
const total_cnt = ref(0) 
const row_size = 5 
const page = ref(1)

const getTodos = async () => {
  try {
    const res = await axios.get('http://localhost:4000/boards/todo_list', {
      params: {
        page: page.value,
        row_size: row_size,
        search_text: ''
      }
    })
    todos.value = res.data.todo_list
    total_cnt.value = res.data.total_cnt
    console.log(total_cnt.value)
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
    <hr />
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li class="page-item"><a class="page-link" href="#">Previous</a></li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item"><a class="page-link" href="#">Next</a></li>
      </ul>
    </nav>
  </div>
</template>


<style scoped>

</style>
