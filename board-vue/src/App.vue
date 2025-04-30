
<template>
  <div class="container">
    <h2>Todo List</h2>  
    <TodoAddForm @add-todo="addTodo" />
    <TodoList :todos="todos" />
  </div>
</template>


<script setup>
import { ref } from 'vue';
import TodoAddForm from './components/TodoAddForm.vue';
import TodoList from './components/TodoList.vue';

const todos = ref([]); 

const deleteTodo = (index) => {
  todos.value.splice(index, 1);
};

const addTodo = (todo) => {
  todos.value.push({
    id: Date.now(), 
    subject: todo.subject,
    completed: false, 
  });
};
</script>


<style>
  .todo {
   color: gray;
   text-decoration: line-through; 
  }
</style>





