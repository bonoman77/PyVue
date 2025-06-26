<script setup>
import Modal from '@/components/ui/Modal.vue'

const emit = defineEmits(['close', 'delete'])

const onClose = () => {
  emit('close')
}

const onDelete = () => {
  emit('delete')
}
</script>

<template>
  <Modal @close="onClose">
    <template #title>
      <h5 class="modal-title">할 일 삭제</h5>
    </template>
    <template #body>
      <p>정말로 이 할 일을 삭제하시겠습니까?</p>
      <p>이 작업은 되돌릴 수 없습니다.</p>
    </template>
    <template #footer>
      <button type="button" class="btn btn-secondary" @click="onClose">취소</button>
      <button type="button" class="btn btn-danger" @click="onDelete">삭제</button>
    </template>
  </Modal>
</template>

<style scoped>
</style>
