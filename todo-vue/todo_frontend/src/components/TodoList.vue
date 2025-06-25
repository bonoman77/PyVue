<script setup>
import { ref } from 'vue';  
import { useRouter } from 'vue-router';
import Modal from '@/components/DeleteModal.vue'

const router = useRouter()
const props = defineProps({
  todos: {
    type: Array,
    required: true
  }, 

})

const emit = defineEmits(['delete-todo', 'toggle-todo'])

const showModal = ref(false)
const todoDeleteId = ref(null)

const openDeleteModal = (todoId) => {
  todoDeleteId.value = todoId
  showModal.value = true

}

const closeModal = () => {
  todoDeleteId.value = null
  showModal.value = false
}

const deleteTodo = () => {
  console.log(todoDeleteId.value)
  emit('delete-todo', todoDeleteId.value)
  showModal.value = false
}

const toggleTodo = (index, event) => {
  emit('toggle-todo', index, event.target.checked)
}

const moveToPage = (todoId) => {
  showModal.value = false
  router.push({ name: 'Todo', params: { todo_id: todoId } })
}

</script>

<template>
    <div v-for="(todo,index) in todos" :key="todo.todo_id" class="card py-1 my-1">
      <div class="card-body p-1 ps-0 d-flex align-items-center justify-content-between" style="cursor: pointer;"
      @click="moveToPage(todo.todo_id)">
        
        <div class="flex-grow-1 d-flex align-items-center">
          <input type="checkbox" :checked="todo.completed"
          @change="toggleTodo(index, $event)" @click.stop=""
          class="form-check-input me-2"  
          >
          <div :class="todo.completed ? 'todo-completed' : ''">{{ todo.title }}</div>
        </div>
        
        <div class="ms-auto">  
          <button type="button" class="btn btn-danger btn-sm" @click.stop="openDeleteModal(todo.todo_id)">Delete</button>
        </div>
      </div>
    </div>
    <teleport to="#modal">
      <Modal v-if="showModal" @close="closeModal" @delete="deleteTodo" />
    </teleport>
</template>

<style scoped>
.card {
  padding-left: 10px;
  padding-right: 3px;
}

.todo-completed {
  text-decoration: line-through;
  color: gray;
}
</style>
