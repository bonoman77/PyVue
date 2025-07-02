<script setup>
import { computed, ref, watch, onMounted } from 'vue'; 
import TodoList from '@/components/todo/TodoList.vue'
import Pagination from '@/components/common/Pagination.vue'
import Button from '@/components/ui/Button.vue'
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
// 검색어를 스토어에서 가져오도록 수정
const searchText = computed({
  get: () => todoStore.searchText,
  set: (value) => todoStore.searchText = value
})
const numberOfPages = computed(() => todoStore.totalPages)

// 컴포넌트 마운트 시 할 일 목록 불러오기
onMounted(() => {
  todoStore.fetchTodos(todoStore.currentPage, todoStore.searchText)
})

// 페이지 변경 시 할 일 목록 불러오기
const getTodos = (page = currentPage.value) => {
  todoStore.fetchTodos(page, searchText.value)
}

// 할 일 삭제
const deleteTodo = async (todoId) => {
  await todoStore.deleteTodo(todoId)
}

// 할 일 완료 상태 토글
const toggleTodo = async (todoId, completed) => {
  await todoStore.toggleTodo(todoId, completed)
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
  router.push({ name: 'TodoWrite' })
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between mb-3">
      <h2>To-Do List</h2>
      <Button 
        variant="primary" 
        size="sm" 
        @click="moveToTodoCreatePage"
      >
        Add Todo
      </Button>
    </div>

    <input type="text" 
    class="form-control mb-2"
    v-model="searchText" 
    placeholder="Search todos..."
    @keyup.enter="searchTodo">
    <div v-if="error" class="text-danger">{{ error }}</div>
    <div v-if="loading" class="text-center py-2">
      Loading...
    </div>
    <div v-else-if="todos.length === 0" class="text-center py-2">
      No todos available.
    </div>
    <TodoList v-else :todos="todos" @delete-todo="deleteTodo" @toggle-todo="toggleTodo"/>
    <hr />
    <Pagination 
      :current-page="currentPage" 
      :total-pages="numberOfPages"
      @page-change="getTodos"
    />
  </div>
</template>

<style scoped>

</style>