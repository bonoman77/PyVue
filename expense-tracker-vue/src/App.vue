<template>
    <Header />
    <div class="container">
    <Balance :total="+total" />
    <IncomeExpenses :income="+income" :expense="+expense" />
    <TransactionList :transactions="transactions" 
    @transactionDeleted="handleTransactionDeleted" />
    <AddTransaction @transactionAdd="handleTransactionAdd"  />
  </div> 
</template>

<script setup>
 import Header from './components/Header.vue'
 import Balance from './components/Balance.vue'
 import IncomeExpenses from './components/IncomeExpenses.vue'
 import TransactionList from './components/TransactionList.vue'
 import AddTransaction from './components/AddTransaction.vue'
 import { useToast } from 'vue-toastification'
 import { ref, computed } from 'vue'

 const toast = useToast()

 const transactions = ref([])

 const total = computed(() => {
    return transactions.value.reduce((acc, transaction) => {
      return acc + transaction.amount
    }, 0)
  }); 

  const income = computed(() => {
    return transactions.value.filter(transaction => transaction.amount > 0).reduce((acc, transaction) => {
      return acc + transaction.amount
    }, 0).toFixed(2)
  }); 

  const expense = computed(() => {
    return transactions.value.filter(transaction => transaction.amount < 0).reduce((acc, transaction) => {
      return acc + transaction.amount
    }, 0).toFixed(2)
  }); 

  const handleTransactionAdd = (transactionData) => {
    transactions.value.push({
      id: generateUniqueId(),
      text: transactionData.text, 
      amount: transactionData.amount, 
    })
  }

  const generateUniqueId = () => {
    const timestamp = new Date().getTime();
    return timestamp;
  }

  const handleTransactionDeleted = (id) => {
    transactions.value = transactions.value.filter(transaction => transaction.id !== id); 
    toast.success('Transaction deleted successfully'); 
  }
</script>