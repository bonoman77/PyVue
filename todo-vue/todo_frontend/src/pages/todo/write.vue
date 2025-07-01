<script setup>
import TodoForm from '@/components/todo/TodoForm.vue'
</script>

<template>
  <div>
    <h4>새 할 일 작성</h4>
    <TodoForm :editing="false" />
  </div>  
</template>

<style scoped>

</style>
