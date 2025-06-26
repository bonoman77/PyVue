<template>
  <div>
    <div class="form-group">
        <label class="form-label">{{ label }}</label>
        <input type="text" class="form-control" :value="modelValue" @input="onInput">
    </div>
    <div v-if="error" class="text-danger">{{ error }}</div>
  </div>
</template>

<script setup>

const props = defineProps({
    label: {
        type: String,
        required: true
    },
    error: {
        type: String,
        required: false
    }, 
    modelValue: {
        type: String,
        required: true
    }
})

const emit = defineEmits(['update:modelValue'])

const onInput = (event) => {
    emit('update:modelValue', event.target.value)
}
</script>

<style scoped>

</style>