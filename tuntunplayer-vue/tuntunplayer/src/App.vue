<template>
  <div class="container">
    <h2>Todo List</h2>
    <TodoSimpleForm @add-todo="onAddTodo"/>

    <div v-show="todos.length === 0">
      추가된 Todo가 없습니다.
    </div>
    <TodoList :todos="todos" @delete="onDelete"/>
  </div>
</template>

<script setup>
  import { ref } from 'vue' 
  import TodoSimpleForm from './components/TodoSimpleForm.vue';
  import TodoList from './components/TodoList.vue';

  const name = ref("SeungKyun");
  const todos = ref([]);

  const greeting = () => {
    name.value = "Hello";
  }

  const onAddTodo = (todo) => {
    todos.value.push(todo);
  };

  const onDelete = (id) => {
    todos.value = todos.value.filter((todo) => todo.id !== id);
  };
</script>



<style scoped>

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

</style>


<!-- Delete -->












