<!-- src/components/common/Pagination.vue -->
<template>
    <nav aria-label="Page navigation">
      <ul class="pagination justify-content-center">
        <li v-if="currentPage > 1" class="page-item">
          <a class="page-link" href="#" @click.prevent="onPageChange(currentPage - 1)">Previous</a>
        </li>
  
        <li 
          v-for="page in totalPages" 
          :key="page"
          class="page-item"
          :class="{ active: currentPage === page }"
        >
          <a class="page-link" href="#" @click.prevent="onPageChange(page)">
            {{ page }}
          </a>
        </li>
  
        <li v-if="currentPage < totalPages" class="page-item">
          <a class="page-link" href="#" @click.prevent="onPageChange(currentPage + 1)">Next</a>
        </li>
      </ul>
    </nav>
  </template>
  
  <script setup>
  const props = defineProps({
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    }
  })
  
  const emit = defineEmits(['page-change'])
  
  const onPageChange = (page) => {
    if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
      emit('page-change', page)
    }
  }
  </script>
  
  <style scoped>
  .page-item {
    cursor: pointer;
  }
  .page-item.disabled .page-link {
    cursor: not-allowed;
    opacity: 0.6;
  }
  </style>