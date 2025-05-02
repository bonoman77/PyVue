
<template>
  <div class="container">
    <h2>Todo List</h2>  
    <input class="form-control" type="text" v-model="searchText" placeholder="Search...">
    <hr />
    <TodoAddForm @add-todo="addTodo" />
    <div v-if="filteredTodos.length === 0">
      No todos found.
    </div>
    <TodoList :todos="filteredTodos" @delete-todo="deleteTodo" @toggle-todo="toggleTodo" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import TodoAddForm from './components/TodoAddForm.vue';
import TodoList from './components/TodoList.vue';
import axios from 'axios';

const todos = ref([]); 
const searchText = ref('');

const filteredTodos = computed(() => {
  return todos.value.filter((todo) => {
    return todo.subject.toLowerCase().includes(searchText.value.toLowerCase());
  });
});

const addTodo = (todo) => {

  axios.post('http://localhost:4000/todo_insert', {
    subjects: todo.subject,
    completed: todo.completed, 
  })
  .then((response) => {
    todos.value.push(response.data);
  })
  .catch((error) => {
    console.error('Error adding todo:', error);
  });

};

const deleteTodo = (index) => {
  todos.value.splice(index, 1);
};

const toggleTodo = (index) => {
  todos.value[index].completed = !todos.value[index].completed;
};

</script>


<style>
  .todo {
   color: gray;
   text-decoration: line-through; 
  }
</style>





