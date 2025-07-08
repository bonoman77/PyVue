<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import _ from 'lodash'
import { useToast } from 'vue-toastification'
import Input from '@/components/ui/Input.vue'
import { useBoardStore } from '@/store/modules/boardStore'
import { useAuthStore } from '@/store/modules/authStore'

const toast = useToast()
const router = useRouter()
const route = useRoute()
const boardStore = useBoardStore()
const authStore = useAuthStore()
const boardId = route.params.id

// 로컬 상태 정의
const board = ref({
    title: '',
    completed: false,
    contents: ''
})
const originalBoard = ref({
    title: '',
    completed: false,
    contents: ''
})

// 스토어에서 로딩 상태 가져오기
const loading = computed(() => boardStore.loading)
const error = computed(() => boardStore.error)

const props = defineProps({
    editing: {
        type: Boolean,
        default: false
    }
})

// 게시글 상세 정보 가져오기
const getBoard = async () => {
    const fetchedBoard = await boardStore.fetchBoardById(boardId)
    
    if (fetchedBoard) {
        board.value = {...fetchedBoard}
        originalBoard.value = {...fetchedBoard}
    }
}

// 편집 모드인 경우 할 일 정보 가져오기
if (props.editing) {
    onMounted(() => {
        getBoard()
    })
}

// 게시글 변경 여부 확인
const boardChanged = computed(() => {
    return !_.isEqual(board.value, originalBoard.value)
})

// 게시글 상태 토글 (화면에서만 상태 변경)
const toggleDisplayBoardStatus = (event) => {
    // 폼 제출 방지
    if (event) event.preventDefault()
    // 화면 상에서만 상태 변경
    board.value.completed = !board.value.completed
}

// 게시글 목록 페이지로 이동
const moveToBoardListPage = () => {
    router.push({ name: 'BoardList' })
}

// 게시글 저장 또는 수정
const updateBoard = async () => {
    if (board.value.title.trim() === '') {
        toast.error("할 일을 입력해주세요.")
        return
    }
    
    const boardData = {
        userId: authStore.user?.userId || 0, // 로그인한 사용자 ID 사용, 없으면 기본값 1
        title: board.value.title,
        completed: board.value.completed,
        contents: board.value.contents
    }
    
    let success = false
    
    if (props.editing) {
        // 게시글 수정
        success = await boardStore.updateBoard(boardId, boardData)
        
        if (success) {
            toast.success("게시글이 성공적으로 수정되었습니다!")
            moveToBoardListPage()
        } else {
            toast.error("게시글 수정에 실패했습니다.")
        }
    } else {
        // 게시글 추가
        success = await boardStore.addBoard(boardData)
        
        if (success) {
            toast.success("게시글이 성공적으로 저장되었습니다!")
            moveToBoardListPage()
        } else {
            toast.error("게시글 저장에 실패했습니다.")
        }
    }
}
</script>

<template>
    <div v-if="loading">Loading...</div>
    <form v-else
    @submit.prevent="updateBoard">
        <div class="row">
            <div class="col-6">
                <Input label="Title" :error="error" v-model="board.title"/>
            </div>
            <div v-if="editing" class="col-6">
                <div class="form-group">
                    <label for="status-btn" class="form-label">Status</label>
                    <button 
                        id="status-btn"
                        type="button"
                        class="btn w-100"
                        :class="board.completed ? 'btn-success' : 'btn-danger'"
                        @click="toggleDisplayBoardStatus"
                    >
                        {{ board.completed ? 'Done' : 'Not Done' }}
                    </button>
                </div>
            </div>
            <div class="col-12">
                <div class="form-group">
                    <label for="contents" class="form-label">Contents</label>
                    <textarea class="form-control" id="contents" v-model="board.contents"></textarea>
                </div>
            </div>
        </div>
        <hr />
        <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="!boardChanged"
        >
            {{ editing ? '수정' : '생성' }}
        </button>
        <button 
            class="btn btn-secondary ms-2"
            @click="moveToBoardListPage"
        >
            취소
        </button>
    </form>
</template>

<style scoped>
</style>
