<script setup>
import { computed, ref, watch, onMounted } from 'vue'; 
import BoardList from '@/components/board/BoardList.vue'
import Pagination from '@/components/common/Pagination.vue'
import Button from '@/components/ui/Button.vue'
import { useRouter } from 'vue-router'
import { useBoardStore } from '@/store/modules/boardStore'

const boardStore = useBoardStore()
const router = useRouter()

// 스토어의 상태를 컴포넌트에서 사용
const posts = computed(() => boardStore.posts)
const error = computed(() => boardStore.error)
const loading = computed(() => boardStore.loading)
const currentPage = computed({
  get: () => boardStore.currentPage,
  set: (value) => boardStore.currentPage = value
})
// 검색어를 스토어에서 가져오도록 수정
const searchText = computed({
  get: () => boardStore.searchText,
  set: (value) => boardStore.searchText = value
})
const numberOfPages = computed(() => boardStore.totalPages)

// 컴포넌트 마운트 시 할 일 목록 불러오기
onMounted(() => {
  boardStore.fetchPosts(boardStore.currentPage, boardStore.searchText)
})

// 페이지 변경 시 할 일 목록 불러오기
const getPosts = (page = currentPage.value) => {
  boardStore.fetchPosts(page, searchText.value)
}

// 게시글 삭제
const deletePost = async (postId) => {
  await boardStore.deletePost(postId)
}

// 게시글 완료 상태 토글
const toggleDisplay = async (postId, completed) => {
  await boardStore.toggleDisplay(postId, completed)
}

// 검색 타이머
let timeout = null
const searchPost = () => {
  clearTimeout(timeout)
  getPosts(1)
}

// 검색어 변경 감지
watch(searchText, () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    getPosts(1)
  }, 1000)
})

// 게시글 생성 페이지로 이동
const moveToBoardCreatePage = () => {
  router.push({ name: 'BoardWrite' })
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between mb-3">
      <h2>게시글 목록</h2>
      <Button 
        variant="primary" 
        size="sm" 
        @click="moveToBoardCreatePage"
      >
        게시글 추가
      </Button>
    </div>

    <input type="text" 
    class="form-control mb-2"
    v-model="searchText" 
    placeholder="게시글 검색..."
    @keyup.enter="searchPost">
    <div v-if="error" class="text-danger">{{ error }}</div>
    <div v-if="loading" class="text-center py-2">
      로딩중...
    </div>
    <div v-else-if="posts.length === 0" class="text-center py-2">
      게시글이 없습니다.
    </div>
    <TodoList v-else :todos="posts" @delete-post="deletePost" @toggle-display="toggleDisplay"/>
    <hr />
    <Pagination 
      :current-page="currentPage" 
      :total-pages="numberOfPages"
      @page-change="getPosts"
    />
  </div>
</template>

<style scoped>

</style>