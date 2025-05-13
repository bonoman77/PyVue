<template>
    <div>
        <h1>Todo Detail</h1>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const todo_id = ref(route.params.todo_id);

</script>

<style scoped>

</style>
