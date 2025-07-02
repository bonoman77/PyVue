<template>
  <div>
    <ul class="list-group">
      <TodoItem 
        v-for="(todo, index) in props.todos" 
        :key="todo.todo_id"
        :todo="todo"
        :index="index"
        @delete="openModal"
        @toggle="toggleTodo"
      />
    </ul>

    <teleport to="body">
      <DeleteModal 
        v-if="showModal" 
        @close="closeModal" 
        @delete="deleteTodo"
      />
    </teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DeleteModal from '@/components/todo/DeleteModal.vue'
import TodoItem from '@/components/todo/TodoItem.vue'

const props = defineProps({
  todos: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['delete-todo', 'toggle-todo'])

const showModal = ref(false)
const selectedTodoId = ref(null)

// 모달 열기
const openModal = (todoId) => {
  selectedTodoId.value = todoId
  showModal.value = true
}

// 모달 닫기
const closeModal = () => {
  showModal.value = false
  selectedTodoId.value = null
}

// 할 일 삭제
const deleteTodo = () => {
  emit('delete-todo', selectedTodoId.value)
  closeModal()
}

// 할 일 상태 토글
const toggleTodo = (todo, index) => {
  if (todo && todo.todo_id) {
    emit('toggle-todo', todo.todo_id, !todo.completed)
  }
}
</script>

<style scoped>
</style>