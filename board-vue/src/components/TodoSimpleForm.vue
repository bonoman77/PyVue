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

<script>
  export default {
    name: 'TodoSimpleForm',
  };
</script>

<style></style>
