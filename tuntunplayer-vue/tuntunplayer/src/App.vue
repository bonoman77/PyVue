

<template>
  <div class="container">
    <h2>Todo List</h2>
    <TodoSimpleForm @add-todo="onAddTodo"/>

    <div v-show="todos.length === 0">
      추가된 Todo가 없습니다.
    </div>
    <div class="card" v-for="todo in todos" :key="todo.id">
      <div class="card-body d-flex">
        <div class="form-check flex-grow-1 align-self-center">
          <input type="checkbox" class="form-check-input" v-model="todo.completed">
          <label class="form-check-label" :class="{ completed: todo.completed }">{{ todo.subject }}</label>
        </div>
        <button class="btn btn-danger" type="button" @click="onDelete(todo.id)">Delete</button>
      </div>
    </div>
  </div>
</template>


<script setup>
  import { ref } from 'vue' 
  import TodoSimpleForm from './components/TodoSimpleForm.vue';

  const todos = ref([]);

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
.completed {
  color: gray;
  text-decoration: line-through;
}
</style>
