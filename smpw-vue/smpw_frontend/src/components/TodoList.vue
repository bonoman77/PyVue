<template>
    <div class="card p-1 mt-2" v-for="(todo, index) in todos" :key="todo.id">
    <div class="card-body p-2 text-start d-flex align-items-center" style="cursor: pointer;"
    @click="moveTodoDetail(todo.todo_id)"
    >
        <div class="flex-grow-1">
        <input type="checkbox" class="ms-1 me-2" :checked="todo.completed" @click.stop="toggleTodo(index, $event)">
        <span :class="{todo: todo.completed}">
            {{ todo.title }}
        </span>
        </div>
        <button class="btn btn-danger btn-sm" type="button" @click.stop="deleteTodo(index)">
        Delete
        </button>
    </div>
    </div>
    <Modal />
</template>

<script setup>
import { useRouter } from 'vue-router';
import Modal from '@/components/Modal.vue';

const components = {
    Modal
}

const router = useRouter();

const props = defineProps({
    todos: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(['delete-todo', 'toggle-todo'])

const deleteTodo = (index) => {
    emit('delete-todo', index)
}

const toggleTodo = (index, event) => {
    emit('toggle-todo', index, event.target.checked)
}

const moveTodoDetail = (todo_id) => {
    router.push({name: 'Todo', params: {todo_id: todo_id}}) 
}
</script>