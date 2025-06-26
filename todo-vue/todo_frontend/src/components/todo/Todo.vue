<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import _ from 'lodash'
import { useToast } from 'vue-toastification'
import Input from '@/components/ui/Input.vue'
import { useTodoStore } from '@/store/modules/todoStore'

const toast = useToast()
const router = useRouter()
const route = useRoute()
const todoStore = useTodoStore()
const todoId = route.params.id

// 로컬 상태 정의
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

// 스토어에서 로딩 상태 가져오기
const loading = computed(() => todoStore.loading)
const error = computed(() => todoStore.error)

const props = defineProps({
    editing: {
        type: Boolean,
        default: false
    }
})

// 할 일 상세 정보 가져오기
const getTodo = async () => {
    const fetchedTodo = await todoStore.fetchTodoById(todoId)
    
    if (fetchedTodo) {
        todo.value = {...fetchedTodo}
        originalTodo.value = {...fetchedTodo}
    }
}

// 편집 모드인 경우 할 일 정보 가져오기
if (props.editing) {
    onMounted(() => {
        getTodo()
    })
}

// 할 일 변경 여부 확인
const todoChanged = computed(() => {
    return !_.isEqual(todo.value, originalTodo.value)
})

// 할 일 상태 토글
const toggleTodoStatus = () => {
    todo.value.completed = !todo.value.completed
}

// 할 일 목록 페이지로 이동
const moveToTodoListPage = () => {
    router.push({ name: 'TodoList' })
}

// 할 일 저장 또는 수정
const updateTodo = async () => {
    if (todo.value.title.trim() === '') {
        toast.error("할 일을 입력해주세요.")
        return
    }
    
    const todoData = {
        title: todo.value.title,
        completed: todo.value.completed,
        contents: todo.value.contents
    }
    
    let success = false
    
    if (props.editing) {
        // 할 일 수정
        success = await todoStore.updateTodo(todoId, todoData)
        
        if (success) {
            toast.success("할 일이 성공적으로 수정되었습니다!")
            moveToTodoListPage()
        } else {
            toast.error("할 일 수정에 실패했습니다.")
        }
    } else {
        // 할 일 추가
        success = await todoStore.addTodo(todoData)
        
        if (success) {
            toast.success("할 일이 성공적으로 저장되었습니다!")
            moveToTodoListPage()
        } else {
            toast.error("할 일 저장에 실패했습니다.")
        }
    }
}
</script>

<template>
    <div v-if="loading">Loading...</div>
    <form v-else
    @submit.prevent="updateTodo">
        <div class="row">
            <div class="col-6">
                <Input label="Title" :error="error" v-model="todo.title"/>
            </div>
            <div v-if="editing" class="col-6">
                <div class="form-group">
                    <label for="status-btn" class="form-label">Status</label>
                    <button type="button" 
                    id="status-btn"
                    class="btn w-100" :class="todo.completed ? 'btn-success' : 'btn-danger'" 
                    @click="toggleTodoStatus">{{ todo.completed ? 'Done' : 'Not Done' }}
                </button>
                </div>
            </div>
            <div class="col-12">
                <div class="form-group">
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
