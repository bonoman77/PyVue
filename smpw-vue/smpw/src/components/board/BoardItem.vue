<template>
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <div>
        <input 
          type="checkbox" 
          :checked="post.display" 
          @change="onToggle($event)"
          @click.stop
          class="form-check-input me-2"
        />
        <router-link 
          :to="{ name: 'BoardDetail', params: { id: post.post_id } }" 
          class="post-title"
          :class="{ 'text-decoration-line-through': post.display }"
        >
          {{ post.title }}
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
    post: {
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
    emit('toggle', props.post, props.index);
  };
  
  const onDelete = () => {
    emit('delete', props.post.post_id, props.index);
  };
  </script>
  
  <style scoped>
  .post-title {
    cursor: pointer;
    color: #212529;
    text-decoration: none;
  }
  
  .post-title:hover {
    color: #0d6efd;
    text-decoration: underline;
  }
  
  .post-title.text-decoration-line-through {
    color: #6c757d;
  }
  </style>