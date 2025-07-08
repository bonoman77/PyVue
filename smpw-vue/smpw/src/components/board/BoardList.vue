<template>
    <div>
      <ul class="list-group">
        <BoardItem 
          v-for="(board, index) in props.boards" 
          :key="board.board_id"
          :board="board"
          :index="index"
          @delete="openModal"
          @toggle-display="toggleDisplay"
        />
      </ul>
  
      <teleport to="body">
        <DeleteModal 
          v-if="showModal" 
          @close="closeModal" 
          @delete="deleteBoard"
        />
      </teleport>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import DeleteModal from '@/components/board/DeleteModal.vue'
  import BoardItem from '@/components/board/BoardItem.vue'
  
  const props = defineProps({
    boards: {
      type: Array,
      required: true
    }
  })
  
  const emit = defineEmits(['delete-board', 'toggle-display'])
  
  const showModal = ref(false)
  const selectedBoardId = ref(null)
  
  // 모달 열기
  const openModal = (boardId) => {
    selectedBoardId.value = boardId
    showModal.value = true
  }
  
  // 모달 닫기
  const closeModal = () => {
    showModal.value = false
    selectedBoardId.value = null
  }
  
  // 게시글 삭제
  const deleteBoard = () => {
    emit('delete-board', selectedBoardId.value)
    closeModal()
  }
  
  // 게시글 상태 토글
  const toggleDisplay = (board, index) => {
    if (board && board.board_id) {
      emit('toggle-display', board.board_id, !board.displayYn)
    }
  }
  </script>
  
  <style scoped>
  </style>