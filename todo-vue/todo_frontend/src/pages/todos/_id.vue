<script setup>
import axios from 'axios'
import { ref, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import _ from 'lodash'
import { useToast } from 'vue-toastification'

const toast = useToast()
const router = useRouter()
const route = useRoute()
const todo = ref('')
const originalTodo = ref('')
const loading = ref(true)
const todoId = route.params.todo_id

const getTodo = async () => {
    try {
        const res = await axios.get(`http://localhost:4000/boards/todo_detail/${todoId}`)
        todo.value = {...res.data.todo_detail}; 
        originalTodo.value = {...res.data.todo_detail};

        loading.value = false
    } catch (err) {
        console.log(err)
    }
}
getTodo(); 

const todoChanged = computed(() => {
    return !_.isEqual(todo.value, originalTodo.value)
})

const toggleTodoStatus = () => {
    todo.value.completed = !todo.value.completed
}

const moveToTodoListPage = () => {
    router.push({ name: 'Todos' })
}

const updateTodo = async () => {
    try {
        await axios.put(`http://localhost:4000/boards/todo_update/${todoId}`, {
            title: todo.value.title,
            completed: todo.value.completed,
            contents: todo.value.contents
        })
        toast.success("할 일이 성공적으로 저장되었습니다!")
        moveToTodoListPage()
    } catch (err) {
        console.log(err)
        toast.error("할 일 저장에 실패했습니다.")
    }
}
</script>

<template>
    <div>
        <h4>Todo Page {{ route.params.todo_id }}</h4>
        <div v-if="loading">Loading...</div>
        <form v-else
        @submit.prevent="updateTodo">
            <div class="row">
                <div class="col-6">
                    <div class="mb-3">
                        <label for="title" class="form-label">Title</label>
                        <input type="text" class="form-control" id="title" v-model="todo.title">
                    </div>
                </div>
                <div class="col-6">
                    <div class="mb-3">
                        <label for="status-btn" class="form-label">Status</label>
                        <button type="button" 
                        id="status-btn"
                        class="btn w-100" :class="todo.completed ? 'btn-success' : 'btn-danger'" 
                        @click="toggleTodoStatus">{{ todo.completed ? 'Done' : 'Not Done' }}
                    </button>
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-primary" :disabled="!todoChanged">Save</button>
            <button class="btn btn-outline-dark ms-2"
            @click="moveToTodoListPage">Cancel</button>
        </form>
    </div>
</template>

<style scoped>

</style>