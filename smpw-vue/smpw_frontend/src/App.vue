
<template>
  <div class="container">
    <h2>Todo List</h2>  
    <input class="form-control" type="text" v-model="searchText" placeholder="Search...">
    <hr />
    <TodoAddForm @add-todo="addTodo" />
    <div v-if="err" class="text text-danger">
      {{ err }}
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
const err = ref('');
const searchText = ref('');

const filteredTodos = computed(() => {
  return todos.value.filter((todo) => {
    return todo.title.toLowerCase().includes(searchText.value.toLowerCase());
  });
});

const getTodos = async () => {
  try {
    const res = await axios.get('http://localhost:4000/boards/todo_list');
    print(res)
    todos.value = res.data;
  } catch (error) {
    console.error('Error fetching todos:', error);
    err.value = 'Error fetching todos';
  }
};

getTodos(); 

const addTodo = async (todo) => {
  err.value = '';
  try {
    const res = await axios.post('http://localhost:4000/boards/todo_insert', {
      title: todo.title,
      completed: todo.completed,
    })
    todos.value.push(res.data);
  } catch (error) {
    console.error('Error adding todo:', error);
    err.value = 'Error adding todo';
  }
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





