<script setup>

</script>


<template>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <router-link :to="{ name: 'Home' }" class="navbar-brand">Main</router-link>

  <ul class="navbar-nav mr-auto">
    <li class="nav-item active">
      <router-link :to="{ name: 'Todos' }" class="nav-link">Todos</router-link>
    </li> 
  </ul>
</nav>
<div class="container">
  <router-view />
</div>
</template>


<style scoped>

</style>
