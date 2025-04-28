
<template>
  <div class="container">
    <h2>Todo List</h2>  
    <form @submit.prevent="onSubmit" class="d-flex">
      <div class="flex-grow-1 mr-2">
        <input class="form-control" type="text" v-model="todo" placeholder="Enter new to-do">
      </div>
      <div class="form-group">
        <button class="btn btn-primary" type="submit">Add</button>
      </div>
    </form>
    {{ todos }}
    <div class="card"> 
      <div class="card-body p-2">
        ㅁ;ㅣㄴ아ㅓㄹ
      </div>
    </div>
  </div>
</template>

<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const todo = ref('');
      const todos = ref([
        {id: 1, subject: '휴대폰 사기'}, 
        {id: 2, subject: '우유 주문하기'}, 
      ]); 

      const onSubmit = () => {
        todos.value.push({
          id: Date.now(), 
          subject: todo.value
        });
      };

      return {
        todo,
        todos, 
        onSubmit, 
      };
    }
  }
</script>

<style>

</style>





