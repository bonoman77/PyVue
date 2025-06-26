<script setup>
import { ref } from 'vue';  
import { useRouter } from 'vue-router';
import Modal from '@/components/DeleteModal.vue'
import List from '@/components/List.vue'

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
    <List :items="todos">
      <template #todo="{ item, index }">
      <div class="card-body p-1 ps-0 d-flex align-items-center justify-content-between" style="cursor: pointer;"
      @click="moveToPage(item.todo_id)">
        
        <div class="flex-grow-1 d-flex align-items-center">
          <input type="checkbox" :checked="item.completed"
          @change="toggleTodo(index, $event)" @click.stop=""
          class="form-check-input me-2"  
          >
          <div :class="item.completed ? 'todo-completed' : ''">{{ item.title }}</div>
        </div>
        
        <div class="ms-auto">  
          <button type="button" class="btn btn-danger btn-sm" @click.stop="openDeleteModal(item.todo_id)">Delete</button>
        </div>
      </div>
      </template>
    </List>
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
