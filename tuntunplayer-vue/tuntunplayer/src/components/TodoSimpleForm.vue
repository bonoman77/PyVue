<template>
    <form action="" @submit.prevent="onSubmit">
      <div class="d-flex">
        <div>
          <input type="text" class="form-control" v-model="todo" placeholder="Enter your todo">
        </div>
        <div>
          <button class="btn btn-primary" type="submit">Add</button>
        </div>
      </div>
      <div v-show="hasError" style="color: red;">
        Please enter a todo  
      </div>  
    </form>
</template>

<script setup>
    import { ref } from 'vue';

    const emit = defineEmits(['add-todo']);

    const todo = ref('');
    const hasError = ref(false);

    const onSubmit = () => {
        if(todo.value.trim() === '') {
            hasError.value = true;
        } else {
            emit('add-todo', {
                id: Date.now(),
                subject: todo.value,
                completed: false
            });
            todo.value = '';
            hasError.value = false;
        }
    };
</script>

<style scoped>

</style>
