<template>
    <Modal>
        <template #title>
            Delete Todo
        </template>
        <template #body>
            Are you sure you want to delete this todo?
        </template>
        <template #footer>
            <button class="btn btn-secondary" type="button" @click="closeModal">Close</button>
            <button class="btn btn-danger" type="button" @click="deleteTodo">Delete</button>
        </template>
    </Modal>
</template>

<script setup>
import Modal from '@/components/Modal.vue';

const components = {
    Modal
}

const emit = defineEmits(['close', 'delete-todo'])

const closeModal = () => {
    emit('close')
}

const deleteTodo = () => {
    emit('delete-todo')
}

</script>

<style scoped>

</style>
