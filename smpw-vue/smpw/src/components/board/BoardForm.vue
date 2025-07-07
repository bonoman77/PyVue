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
const postId = route.params.id

// 로컬 상태 정의
const post = ref({
    title: '',
    display: false,
    contents: ''
})
const originalPost = ref({
    title: '',
    display: false,
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

// 할 일 상세 정보 가져오기
const getPost = async () => {
    const fetchedPost = await boardStore.fetchPostById(postId)
    
    if (fetchedPost) {
        post.value = {...fetchedPost}
        originalPost.value = {...fetchedPost}
    }
}

// 편집 모드인 경우 할 일 정보 가져오기
if (props.editing) {
    onMounted(() => {
        getPost()
    })
}

// 게시글 변경 여부 확인
const postChanged = computed(() => {
    return !_.isEqual(post.value, originalPost.value)
})

// 게시글 상태 토글 (화면에서만 상태 변경)
const togglePostStatus = (event) => {
    // 폼 제출 방지
    if (event) event.preventDefault()
    // 화면 상에서만 상태 변경
    post.value.display = !post.value.display
}

// 게시글 목록 페이지로 이동
const moveToPostListPage = () => {
    router.push({ name: 'Posts' })
}

// 게시글 저장 또는 수정
const updatePost = async () => {
    if (post.value.title.trim() === '') {
        toast.error("게시글을 입력해주세요.")
        return
    }
    
    const postData = {
        userId: authStore.user?.userId || 0, // 로그인한 사용자 ID 사용, 없으면 기본값 0
        title: post.value.title,
        display: post.value.display,
        contents: post.value.contents
    }
    
    let success = false
    
    if (props.editing) {
        // 게시글 수정
        success = await boardStore.updatePost(postId, postData)
        
        if (success) {
            toast.success("게시글이 성공적으로 수정되었습니다!")
            moveToPostListPage()
        } else {
            toast.error("게시글 수정에 실패했습니다.")
        }
    } else {
        // 게시글 추가
        success = await boardStore.addPost(postData)
        
        if (success) {
            toast.success("게시글이 성공적으로 저장되었습니다!")
            moveToPostListPage()
        } else {
            toast.error("게시글 저장에 실패했습니다.")
        }
    }
}
</script>

<template>
    <div v-if="loading">Loading...</div>
    <form v-else
    @submit.prevent="updatePost">
        <div class="row">
            <div class="col-6">
                <Input label="Title" :error="error" v-model="post.title"/>
            </div>
            <div v-if="editing" class="col-6">
                <div class="form-group">
                    <label for="status-btn" class="form-label">Status</label>
                    <button 
                        id="status-btn"
                        type="button"
                        class="btn w-100"
                        :class="post.display ? 'btn-success' : 'btn-danger'"
                        @click="togglePostStatus"
                    >
                        {{ post.display ? 'Done' : 'Not Done' }}
                    </button>
                </div>
            </div>
            <div class="col-12">
                <div class="form-group">
                    <label for="contents" class="form-label">Contents</label>
                    <textarea class="form-control" id="contents" v-model="post.contents"></textarea>
                </div>
            </div>
        </div>
        <hr />
        <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="!postChanged"
        >
            {{ editing ? '수정' : '생성' }}
        </button>
        <button 
            class="btn btn-secondary ms-2"
            @click="moveToPostListPage"
        >
            취소
        </button>
    </form>
</template>

<style scoped>
</style>
