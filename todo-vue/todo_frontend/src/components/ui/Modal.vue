<script setup>
import { onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['close'])

// 모달 닫기
const onClose = () => {
  emit('close')
}

// ESC 키로 모달 닫기
const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    onClose()
  }
}

// 컴포넌트 마운트 시 이벤트 리스너 등록
onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

// 컴포넌트 언마운트 시 이벤트 리스너 제거
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<template>
  <div class="modal-backdrop" @click="onClose">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <slot name="title">
          <h5 class="modal-title">Modal Title</h5>
        </slot>
        <button type="button" class="btn-close" @click="onClose"></button>
      </div>
      <div class="modal-body">
        <slot name="body">
          <p>Modal Body</p>
        </slot>
      </div>
      <div class="modal-footer">
        <slot name="footer">
          <button type="button" class="btn btn-secondary" @click="onClose">닫기</button>
        </slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: white;
  border-radius: 5px;
  width: 500px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-body {
  padding: 1rem;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>