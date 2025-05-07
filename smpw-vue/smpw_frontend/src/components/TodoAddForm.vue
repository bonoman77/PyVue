<template>
    <form @submit.prevent="onSubmit">
      <div class="d-flex">
        <div class="flex-grow-1 mr-2">
          <input class="form-control" type="text" v-model="todo" placeholder="Enter new to-do">
        </div>
        <div class="form-group">
          <button class="btn btn-primary" type="submit">Add</button>
        </div>
      </div>
      <div v-show="hasError" class="text-danger">
        Please enter a valid todo.
      </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';
import { useToast } from 'vue-toastification';

const toast = useToast();
const todo = ref('');
const hasError = ref(false); 

const emit = defineEmits(['add-todo'])

const onSubmit = () => {
  if (todo.value === '') {
    hasError.value = true;
  } else { 

    const todoData = {
      id: Date.now(),
      title: todo.value,
      completed: false,
    }
    emit('add-todo', todoData)
    
    // toast.success('Todo added successfully');
    hasError.value = false;
    todo.value = ''; 
  }
};

</script>

<style></style>
