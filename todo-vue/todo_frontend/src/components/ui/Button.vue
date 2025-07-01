<!-- src/components/ui/Button.vue -->
<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  block: {
    type: Boolean,
    default: false
  }
})

const buttonClasses = computed(() => {
  return [
    'btn',
    `btn-${props.variant}`,
    { [`btn-${props.size}`]: props.size !== 'md' },
    { 'w-100': props.block },
    { 'disabled': props.disabled || props.loading }
  ]
})

const isDisabled = computed(() => props.disabled || props.loading)
</script>

<template>
  <button
    :type="type"
    :class="buttonClasses"
    :disabled="isDisabled"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
    <slot></slot>
  </button>
</template>

<style scoped>
.btn {
  font-weight: 500;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1.125rem;
}

.btn-primary {
  background-color: #4361ee;
  border-color: #4361ee;
  color: white;
}

.btn-primary:hover:not(.disabled) {
  background-color: #3a56d4;
  border-color: #3a56d4;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
  color: white;
}

.btn-success {
  background-color: #2ecc71;
  border-color: #2ecc71;
  color: white;
}

.btn-danger {
  background-color: #e74c3c;
  border-color: #e74c3c;
  color: white;
}

.btn-warning {
  background-color: #f39c12;
  border-color: #f39c12;
  color: white;
}

.btn-info {
  background-color: #3498db;
  border-color: #3498db;
  color: white;
}

.disabled {
  opacity: 0.65;
  cursor: not-allowed;
}
</style>