<template>
    <div>
      <ul class="list-group">
        <BoardItem 
          v-for="(post, index) in props.posts" 
          :key="post.post_id"
          :post="post"
          :index="index"
          @delete="openModal"
          @toggle-display="toggleDisplay"
        />
      </ul>
  
      <teleport to="body">
        <DeleteModal 
          v-if="showModal" 
          @close="closeModal" 
          @delete="deletePost"
        />
      </teleport>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import DeleteModal from '@/components/board/DeleteModal.vue'
  import BoardItem from '@/components/board/BoardItem.vue'
  
  const props = defineProps({
    posts: {
      type: Array,
      required: true
    }
  })
  
  const emit = defineEmits(['delete-post', 'toggle-display'])
  
  const showModal = ref(false)
  const selectedPostId = ref(null)
  
  // 모달 열기
  const openModal = (postId) => {
    selectedPostId.value = postId
    showModal.value = true
  }
  
  // 모달 닫기
  const closeModal = () => {
    showModal.value = false
    selectedPostId.value = null
  }
  
  // 게시글 삭제
  const deletePost = () => {
    emit('delete-post', selectedPostId.value)
    closeModal()
  }
  
  // 게시글 상태 토글
  const toggleDisplay = (post, index) => {
    if (post && post.post_id) {
      emit('toggle-display', post.post_id, !post.display)
    }
  }
  </script>
  
  <style scoped>
  </style>