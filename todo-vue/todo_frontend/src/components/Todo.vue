<script setup>
import axios from 'axios'
import { ref, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import _ from 'lodash'
import { useToast } from 'vue-toastification'

const toast = useToast()
const router = useRouter()
const route = useRoute()
const todo = ref({
    title: '',
    completed: false,
    contents: ''
})
const originalTodo = ref({
    title: '',
    completed: false,
    contents: ''
})

const loading = ref(false)
const todoId = route.params.todo_id
const hasError = ref(false)

const props = defineProps({
    editing: {
        type: Boolean,
        default: false
    }
})

const getTodo = async () => {
    loading.value = true
    try {
        const res = await axios.get(`http://localhost:4000/boards/todo_detail/${todoId}`)
        todo.value = {...res.data.todo_detail}; 
        originalTodo.value = {...res.data.todo_detail};

        loading.value = false
    } catch (err) {
        console.log(err)
        loading.value = false
    }
}

if (props.editing) {
    getTodo(); 
}

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
    if (todo.value.title.trim() === '') {
        toast.error("할 일을 입력해주세요.")
        return
    }
    try {
        let res; 
        const params = {
            title: todo.value.title,
            completed: todo.value.completed,
            contents: todo.value.contents
        }

        if (props.editing) {
            res = await axios.put(`http://localhost:4000/boards/todo_update/${todoId}`, params)
        } else {
            res = await axios.post(`http://localhost:4000/boards/todo_insert`, params)
        }

        if (res.status === 200) {
            if (props.editing) {
                toast.success("할 일이 성공적으로 수정되었습니다!")
            } else {
                toast.success("할 일이 성공적으로 저장되었습니다!")
            }
            moveToTodoListPage()
        }
    } catch (err) {
        console.log(err)
        toast.error("할 일 저장에 실패했습니다.")
    }
}
</script>

<template>
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
            <div v-if="editing" class="col-6">
                <div class="mb-3">
                    <label for="status-btn" class="form-label">Status</label>
                    <button type="button" 
                    id="status-btn"
                    class="btn w-100" :class="todo.completed ? 'btn-success' : 'btn-danger'" 
                    @click="toggleTodoStatus">{{ todo.completed ? 'Done' : 'Not Done' }}
                </button>
                </div>
            </div>
            <div class="col-12">
                <div class="mb-3">
                    <label for="contents" class="form-label">Contents</label>
                    <textarea class="form-control" id="contents" v-model="todo.contents"></textarea>
                </div>
            </div>
        </div>
        <button type="submit" class="btn btn-primary" :disabled="!todoChanged">
            {{ editing ? 'Update' : 'Create' }}
        </button>
        <button class="btn btn-outline-dark ms-2"
        @click="moveToTodoListPage">Cancel</button>
    </form>
</template>

<style scoped>
</style>    