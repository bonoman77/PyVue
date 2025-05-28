<template>

    <div class="form-group text-start">
        <label for="title">{{label}}</label>
        <div>
            <input type="text" id="title"
            :value="subject"
            @input="onInput">
        </div>
        <span v-if="error" class="text-danger">{{ error }}</span>
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
        required: true
    },
    subject: {
        type: String,
        required: true
    }
})

const emit = defineEmits(['update:subject'])

const onInput = () => {
    emit('update:subject', $event.target.value)
}

</script>

<style scoped>

</style>    