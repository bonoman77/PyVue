<template>
    <div class="card p-1 mt-2" v-for="(item, index) in items" :key="item.id">
        <slot :item="item" :index="index"></slot>
    </div>
</template>

<script setup>
const props = defineProps({
    items: {
        type: Array,
        required: true
    }
})

</script>

<style scoped>

</style>
