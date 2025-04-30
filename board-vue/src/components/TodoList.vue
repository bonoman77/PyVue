<template>
    <div class="card p-1 mt-2" v-for="(todo, index) in todos" :key="todo.id">
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
</template>

<script setup>
const props = defineProps({
    todos: {
        type: Array,
        required: true
    }
})

</script>