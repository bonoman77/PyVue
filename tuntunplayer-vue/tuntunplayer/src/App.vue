<template>
  <div class="container">
    <h2>Todo List</h2>

    <input type="text" class="form-control" v-model="searchText" placeholder="Search">
    <hr />
    <TodoSimpleForm @add-todo="onAddTodo"/>

    <div v-show="!filteredTodos.length">
      There is nothing to display.
    </div>
    <TodoList :todos="filteredTodos" @delete="onDelete" @toggle-todo="onToggleTodo" />  
  </div>
</template>

<script setup>
  import { ref, computed } from 'vue' 
  import TodoSimpleForm from './components/TodoSimpleForm.vue';
  import TodoList from './components/TodoList.vue';

  const todos = ref([]);
  const searchText = ref('');
  const filteredTodos = computed(() => {
    return todos.value.filter((todo) => todo.subject.includes(searchText.value));
  });

  const onAddTodo = (todo) => {
    axios.post('http://localhost:3000/todos', todo)
    todos.value.push(todo);
  };

  const onDelete = (id) => {
    todos.value = todos.value.filter((todo) => todo.id !== id);
  };

  const onToggleTodo = (id) => {
    todos.value = todos.value.map((todo) => {
      if(todo.id === id) {
        todo.completed = !todo.completed;
      }
      return todo;
    });
  };

  const onSearchTodo = (search) => {
    todos.value = todos.value.filter((todo) => todo.subject.includes(search));
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


















