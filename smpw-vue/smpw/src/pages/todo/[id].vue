<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTodoStore } from '@/store/modules/todoStore'
import TodoForm from '@/components/todo/TodoForm.vue'

const route = useRoute()
const todoStore = useTodoStore()
const todoId = route.params.id

// 컴포넌트 마운트 시 할 일 상세 정보 불러오기
onMounted(async () => {
  await todoStore.fetchTodoById(todoId)
})
</script>

<template>
  <div>
    <h4>할 일 상세</h4>
    <TodoForm :editing="true" />
  </div>  
</template>

<style scoped>

</style>