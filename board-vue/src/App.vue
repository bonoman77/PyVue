<script>
export default {
  setup() {
    const name = 'Seungkyun';

    const greeting = (name) => {
      return `Hello ${name}`;
    };
    return {
      name,
      greeting
    };
  }
}
</script>

<template>
  <div>Hello {{ greeting('Seungkyun') }}</div>
</template>

<style>

</style>
