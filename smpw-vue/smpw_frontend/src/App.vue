
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
    <hr />
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li class="page-item"><a class="page-link" href="#">Previous</a></li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item"><a class="page-link" href="#">Next</a></li>
      </ul>
    </nav>
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
const page = ref(1);
const totalCount = ref(0);

const filteredTodos = computed(() => {
  return todos.value.filter((todo) => {
    return todo.title.toLowerCase().includes(searchText.value.toLowerCase());
  });
});

const getTodos = async () => {
  try {
    const res = await axios.get('http://localhost:4000/boards/todo_list');
    todos.value = res.data.todo_list;
    totalCount.value = res.data.todo_list.length;
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
    console.log(res.data)
    todos.value.push(res.data);
  } catch (error) {
    console.error('Error adding todo:', error);
    err.value = 'Error adding todo';
  }
};

const deleteTodo = async (index) => {
  err.value = '';
  const todoId = todos.value[index].todo_id;
  try {
    await axios.delete(`http://localhost:4000/boards/todo_delete/${todoId}`);
    todos.value.splice(index, 1);
  } catch (error) {
    console.error('Error deleting todo:', error);
    err.value = 'Error deleting todo';
  }
};

const toggleTodo = async (index) => {
  err.value = '';
  const todoId = todos.value[index].todo_id;
  try {
    await axios.patch(`http://localhost:4000/boards/todo_toggle/${todoId}/${+!todos.value[index].completed}`);
    todos.value[index].completed = !todos.value[index].completed;
  } catch (error) {
    console.error('Error toggling todo:', error);
    err.value = 'Error toggling todo';
  }
};

</script>


<style>
  .todo {
   color: gray;
   text-decoration: line-through; 
  }
</style>





