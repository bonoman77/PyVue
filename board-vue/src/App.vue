
<template>
  <div class="container">
    <h2>Todo List</h2>  
    <TodoSimpleForm />
    
    <div v-if="todos.length === 0" class="text-muted">
      No todos available.
    </div>
    <div class="card p-1" v-for="(todo, index) in todos" :key="todo.id">
      <div class="card-body p-2 text-start d-flex align-items-center">
        <div class="form-check flex-grow-1">
          <input class="form-check-input" type="checkbox" v-model="todo.completed">
          <label class="form-check-label" :class="{todo: todo.completed}">
            &nbsp;{{ todo.subject }}
          </label>
        </div>
        <button class="btn btn-danger btn-sm" type="button" @click="deleteTodo(index)">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import { ref } from 'vue';
  import TodoSimpleForm from './components/TodoSimpleForm.vue';

  export default {
    components: {
      TodoSimpleForm,
    },
    
    setup() {
      const todo = ref('');
      const todos = ref([]); 

      const hasError = ref(false); 
      const deleteTodo = (index) => {
        todos.value.splice(index, 1);
      };
      const onSubmit = () => {
        if (todo.value === '') {
          hasError.value = true;
        } else { 
          todos.value.push({
            id: Date.now(), 
            subject: todo.value,
            completed: false, 
          });
          hasError.value = false;
          todo.value = ''; 
        }
      };

      return {
        todo,
        todos, 
        hasError,
        onSubmit, 
        deleteTodo
      };
    }
  }
</script>

<style>
  .todo {
   color: gray;
   text-decoration: line-through; 
  }
</style>





