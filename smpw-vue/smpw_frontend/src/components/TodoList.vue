<template>

<List :items="todos">
    <template #default="{item, index}">
        <div class="card-body p-2 text-start d-flex align-items-center" style="cursor: pointer;"
        @click="moveTodoDetail(item.todo_id)"
        >
            <div class="flex-grow-1">
            <input type="checkbox" class="ms-1 me-2" :checked="item.completed" @click.stop="toggleTodo(index, $event)">
            <span :class="{todo: item.completed}">
                {{ item.title }}
            </span>
            </div>
            <button class="btn btn-danger btn-sm" type="button" 

            @click.stop="openModal(item.todo_id)">
            Delete
            </button>
        </div>
    </template>
</List>

    <Modal v-if="modalVisible" @close="closeModal" @delete-todo="deleteTodo" />
</template>

<script setup>
import { useRouter } from 'vue-router';
import Modal from '@/components/DeleteModal.vue';
import { ref } from 'vue';
import List from '@/components/List.vue';

const modalVisible = ref(false);
const todoDeleteId = ref(null);

const components = {
    Modal,
    List
}

const router = useRouter();

const props = defineProps({
    todos: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(['delete-todo', 'toggle-todo', 'close', 'delete-todo'])

const openModal = (todo_id) => {
    todoDeleteId.value = todo_id;
    modalVisible.value = true;
}

const closeModal = () => {
    todoDeleteId.value = null;
    modalVisible.value = false;
}

const deleteTodo = () => {
    emit('delete-todo', todoDeleteId.value)
    modalVisible.value = false;
    todoDeleteId.value = null;
}

const toggleTodo = (index, event) => {
    emit('toggle-todo', index, event.target.checked)
}

const moveTodoDetail = (todo_id) => {
    router.push({name: 'Todo', params: {todo_id: todo_id}}) 
}
</script>