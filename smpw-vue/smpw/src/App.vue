<script setup>
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
</script>

<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <Header />
    <main class="flex-grow-1">
      <div class="container-fluid py-4">
        <router-view />
      </div>
    </main>
    <Footer />
  </div>
</template>

<style scoped>
</style>