<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBoardStore } from '@/store/modules/boardStore'
import BoardForm from '@/components/board/BoardForm.vue'

const route = useRoute()
const boardStore = useBoardStore()
const boardId = route.params.id

// 컴포넌트 마운트 시 할 일 상세 정보 불러오기
onMounted(async () => {
  await boardStore.fetchBoardById(boardId)
})
</script>

<template>
  <div>
    <h4>게시글 상세</h4>
    <BoardForm :editing="true" />
  </div>  
</template>

<style scoped>

</style>