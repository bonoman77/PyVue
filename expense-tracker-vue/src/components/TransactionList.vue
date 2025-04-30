<template>
    <h3>History</h3>
    <ul id="list" class="list">
        <li 
        v-for="transaction in transactions"
        :key="transaction.id"
        :class="transaction.amount < 0 ? 'minus' : 'plus'"
        >
            {{transaction.text}} <span>{{transaction.amount}}</span><span @click="deleteTransaction(transaction.id)" class="delete-btn">x</span>  
        </li>
    </ul>
</template>

<script setup>
import { defineProps } from 'vue'

const emit = defineEmits(['deleteTransaction'])

const props = defineProps({
    transactions: Array
})

const deleteTransaction = (id) => {
  emit('transactionDeleted', id)
}
</script>

<style></style>