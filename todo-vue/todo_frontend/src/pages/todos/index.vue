<script setup>
import { computed, ref, watch } from 'vue'; 
import TodoForm from '@/components/TodoForm.vue'
import TodoList from '@/components/TodoList.vue'
import axios from 'axios'


const todos = ref([])
const error = ref('')
const totalCnt = ref(0) 
const rowSize = 5 
const currentPage = ref(1)
const searchText = ref('')
const numberOfPages = computed(() => {
  return Math.ceil(totalCnt.value / rowSize)
})

const getTodos = async (page = currentPage.value) => {
  currentPage.value = page
  try {
    const res = await axios.get('http://localhost:4000/boards/todo_list', {
      params: {
        page: currentPage.value,
        row_size: rowSize,
        search_text: searchText.value
      }
    })
    todos.value = res.data.todo_list
    totalCnt.value = res.data.total_cnt
    console.log(totalCnt.value)
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
    getTodos(1); 
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
    getTodos()
  } catch (err) {
    console.log(err)
    error.value = 'Failed to delete todo' 
  }
}

const toggleTodo = async (index, checked) => {
  error.value = ''
  try {
    const todo_id = todos.value[index].todo_id
    await axios.patch('http://localhost:4000/boards/todo_toggle/' + todo_id, {
      completed: checked
    })
    todos.value[index].completed = checked
  } catch (err) {
    console.log(err)
    error.value = 'Failed to toggle todo' 
  }
}

let timeout = null; 
const searchTodo = () => {
  clearTimeout(timeout)
  getTodos(1)
}
watch(searchText, () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    getTodos(1)
  }, 1000)
})

// const filteredTodos = computed(() => {
//   if (searchText.value){
//     return todos.value.filter((todo) => {
//       return todo.title.toLowerCase().includes(searchText.value.toLowerCase())
//     })
//   }
//   return todos.value
// })

</script>


<template>
  <div>
    <h2>To-Do List</h2>

    <input type="text" 
    class="form-control mb-2"
    v-model="searchText" 
    placeholder="Search todos..."
    @keyup.enter="searchTodo">
    <TodoForm @add-todo="addTodo"/>
    <div class="text-danger">{{ error }}</div>
    <div v-if="todos.length === 0" class="text-center py-2">
      No todos available.
    </div>
    <TodoList :todos="todos" @delete-todo="deleteTodo" @toggle-todo="toggleTodo"/>
    <hr />
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li v-if="currentPage > 1" class="page-item">
          <a style="cursor: pointer;" class="page-link" @click="getTodos(currentPage - 1)">Previous</a>
        </li>

        <li v-for="page in numberOfPages" :key="page" 
        class="page-item" 
        :class="currentPage === page ? 'active' : ''"
        @click="currentPage = page" 
        >
          <a style="cursor: pointer;" class="page-link" @click="getTodos(page)">
            {{page}}
          </a>
        </li>
        <li v-if="currentPage < numberOfPages" class="page-item">
          <a style="cursor: pointer;" class="page-link" @click="getTodos(currentPage + 1)">Next</a>
        </li>
      </ul>
    </nav>
  </div>
</template>


<style scoped>

</style>
