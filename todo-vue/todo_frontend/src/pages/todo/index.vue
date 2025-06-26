<script setup>
import { computed, ref, watch, onMounted } from 'vue'; 
import TodoForm from '@/components/todo/TodoForm.vue'
import TodoList from '@/components/todo/TodoList.vue'
import { useRouter } from 'vue-router'
import { useTodoStore } from '@/store/modules/todoStore'

const todoStore = useTodoStore()
const router = useRouter()

// 스토어의 상태를 컴포넌트에서 사용
const todos = computed(() => todoStore.todos)
const error = computed(() => todoStore.error)
const loading = computed(() => todoStore.loading)
const currentPage = computed({
  get: () => todoStore.currentPage,
  set: (value) => todoStore.currentPage = value
})
const searchText = ref('')
const numberOfPages = computed(() => todoStore.totalPages)

// 컴포넌트 마운트 시 할 일 목록 불러오기
onMounted(() => {
  todoStore.fetchTodos()
})

// 페이지 변경 시 할 일 목록 불러오기
const getTodos = (page = currentPage.value) => {
  todoStore.fetchTodos(page, searchText.value)
}

// 할 일 추가
const addTodo = async (todo) => {
  const success = await todoStore.addTodo({
    title: todo.title,
    completed: todo.completed,
    contents: todo.contents,
  })
  
  if (success) {
    // 첫 페이지로 이동
    getTodos(1)
  }
}

// 할 일 삭제
const deleteTodo = async (todoId) => {
  await todoStore.deleteTodo(todoId)
}

// 할 일 완료 상태 토글
const toggleTodo = async (index, checked) => {
  const todoId = todos.value[index].todo_id
  await todoStore.toggleTodo(todoId, checked)
}

// 검색 타이머
let timeout = null
const searchTodo = () => {
  clearTimeout(timeout)
  getTodos(1)
}

// 검색어 변경 감지
watch(searchText, () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    getTodos(1)
  }, 1000)
})

// 할 일 생성 페이지로 이동
const moveToTodoCreatePage = () => {
  router.push({ name: 'TodoCreate' })
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between mb-3">
      <h2>To-Do List</h2>
      <button type="button" class="btn btn-primary btn-sm" @click="moveToTodoCreatePage">Add Todo</button>
    </div>

    <input type="text" 
    class="form-control mb-2"
    v-model="searchText" 
    placeholder="Search todos..."
    @keyup.enter="searchTodo">
    <TodoForm @add-todo="addTodo"/>
    <div v-if="error" class="text-danger">{{ error }}</div>
    <div v-if="loading" class="text-center py-2">
      Loading...
    </div>
    <div v-else-if="todos.length === 0" class="text-center py-2">
      No todos available.
    </div>
    <TodoList v-else :todos="todos" @delete-todo="deleteTodo" @toggle-todo="toggleTodo"/>
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