<template>
  <li class="list-group-item d-flex justify-content-between align-items-center">
    <div>
      <input 
        type="checkbox" 
        :checked="todo.completed" 
        @change="onToggle($event)"
        class="form-check-input me-2"
      />
      <router-link 
        :to="{ name: 'TodoDetail', params: { id: todo.todo_id } }" 
        class="todo-title"
        :class="{ 'text-decoration-line-through': todo.completed }"
      >
        {{ todo.title }}
      </router-link>
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
  todo: {
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
  emit('toggle', props.todo, props.index);
};

const onDelete = () => {
  emit('delete', props.todo.todo_id, props.index);
};
</script>

<style scoped>
.todo-title {
  cursor: pointer;
  color: #212529;
  text-decoration: none;
}

.todo-title:hover {
  color: #0d6efd;
  text-decoration: underline;
}

.todo-title.text-decoration-line-through {
  color: #6c757d;
}
</style>