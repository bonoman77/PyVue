<template>
  <div>
    <div class="card" v-for="todo in todos" :key="todo.id">
      <div class="card-body d-flex">
        <div class="form-check flex-grow-1 align-self-center">
     
          <input type="checkbox" class="form-check-input" 
            :checked="todo.completed"
            @change="onToggleTodo(todo.id)"
          />
     
          <label class="form-check-label" :class="{ completed: todo.completed }">{{ todo.subject }}</label>
        </div>
        <button class="btn btn-danger btn-sm" type="button" @click="onDelete(todo.id)">Delete</button>
      </div>
    </div>
  </div>
</template>

<script setup>
  const props = defineProps({
    todos: {
      type: Array,
      required: true
    }
  });

  const emit = defineEmits(['delete', 'toggle-todo']);

  const onDelete = (id) => {
    emit('delete', id);
  
  };

  const onToggleTodo = (id) => {
    emit('toggle-todo', id);   
  };
</script>

<style scoped>
.card {
  padding: 0em; 
  margin-top: 8px; 
}
.completed {
  color: gray;
  text-decoration: line-through;
}
</style>







