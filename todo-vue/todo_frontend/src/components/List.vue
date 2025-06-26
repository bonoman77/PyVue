<template>
    <div v-for="(item,index) in items" :key="item.id" class="card py-1 my-1">  
        <slot name="todo" :item="item" :index="index"></slot>
    </div>

</template>

<script setup>

defineProps({
    items: {
        type: Array,
        required: true
    }
})

</script>

<style scoped>

</style>