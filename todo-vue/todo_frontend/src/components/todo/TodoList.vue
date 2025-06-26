<template>
  <div>
    <ul class="list-group">
      <li v-for="(todo, index) in props.todos" :key="todo.todo_id" class="list-group-item d-flex justify-content-between align-items-center">
        <div>
          <input 
            type="checkbox" 
            :checked="todo.completed" 
            @change="toggleTodo(index, $event)"
            class="form-check-input me-2"
          />
          <span :class="{ 'text-decoration-line-through': todo.completed }">{{ todo.title }}</span>
        </div>
        <div>
          <router-link :to="{ name: 'TodoDetail', params: { id: todo.todo_id } }" class="btn btn-sm btn-info me-1">
            상세
          </router-link>
          <button @click="openModal(todo.todo_id)" class="btn btn-sm btn-danger">
            삭제
          </button>
        </div>
      </li>
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
const toggleTodo = (index, event) => {
  emit('toggle-todo', index, event.target.checked)
}
</script>

<style scoped>
</style>