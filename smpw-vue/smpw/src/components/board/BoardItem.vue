<template>
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <div>
        <input 
          type="checkbox" 
          :checked="board.displayYn" 
          @change="onToggle($event)"
          @click.stop
          class="form-check-input me-2"
        />
        <router-link 
          :to="{ name: 'BoardDetail', params: { id: board.boardId } }" 
          class="board-title"
          :class="{ 'text-decoration-line-through': board.displayYn }"
        >
          {{ board.title }}
        </router-link>
      </div>
      <div class="ms-auto me-3 text-muted">
        {{ board.userName }}
      </div>
      <div>
        <Button 
          variant="danger" 
          size="sm" 
          @click="onDelete"
        >
          삭제
        </Button>
      </div>
    </li>
  </template>
  
  <script setup>
  import Button from '@/components/ui/Button.vue';
  
  const props = defineProps({
    board: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  });
  
  const emit = defineEmits(['toggle', 'delete']);
  
  const onToggle = (event) => {
    emit('toggle', props.board, props.index);
  };
  
  const onDelete = () => {
    emit('delete', props.board.boardId, props.index);
  };
  </script>
  
  <style scoped>
  .board-title {
    cursor: pointer;
    color: #212529;
    text-decoration: none;
  }
  
  .board-title:hover {
    color: #0d6efd;
    text-decoration: underline;
  }
  
  .board-title.text-decoration-line-through {
    color: #6c757d;
  }
  </style>