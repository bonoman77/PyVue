<script setup>
import Todo from '@/components/todo/Todo.vue'
</script>

<template>
  <div>
    <h4>새 할 일 작성</h4>
    <Todo :editing="false" />
  </div>  
</template>

<style scoped>

</style>
