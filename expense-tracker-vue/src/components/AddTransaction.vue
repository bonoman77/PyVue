<template>
    <h3>Add new transaction</h3>
    <form id="form" @submit.prevent="onSubmit">
    <div class="form-control">
        <label for="text">Text</label>
        <input type="text" id="text" v-model="text" placeholder="Enter text..." />
    </div>
    <div class="form-control">
        <label for="amount"
        >Amount <br />
        (negative - expense, positive - income)</label
        >
        <input type="text" id="amount" v-model="amount" placeholder="Enter amount..." />
    </div>
    <button class="btn">Add transaction</button>
    </form>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'vue-toastification'

const text = ref('')
const amount = ref(0)
const toast = useToast()

const emit = defineEmits(['transactionAdd'])

const onSubmit = () => {
    if (text.value.trim() === '' || amount.value === 0) {
        toast.error('Please enter a text and amount')
        return
    }

    const transactionData = {
        text: text.value,
        amount: parseFloat(amount.value),
    }

    emit('transactionAdd', transactionData)

    text.value = '';
    amount.value = 0; 
    toast.success('Transaction added successfully')
}
</script>
