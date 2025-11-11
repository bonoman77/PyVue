

<template>
  <div class="container">
    {{ name }}
  </div>
  <button class="btn btn-primary" v-on:click="consoleLog">Click me</button>
</template>


<script setup>
import { ref } from 'vue'

const name = ref('Kossie Coder'); 
const consoleLog = () => {
  console.log('test');
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
