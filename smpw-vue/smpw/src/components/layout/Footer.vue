<!-- src/components/layout/Footer.vue -->
<script setup>
import { computed } from 'vue';

const currentYear = computed(() => new Date().getFullYear());
</script>

<template>
  <footer class="footer mt-auto py-3 bg-light">
    <div class="container">
      <div class="row py-2">
        <div class="col-md-6 mb-2 mb-md-0">
          <p class="mb-0 text-muted"> {{ currentYear }} SMPW. All rights reserved.</p>
        </div>
        <div class="col-md-6 text-md-end">
          <router-link to="/privacy-policy" class="text-decoration-none text-muted me-3">개인정보처리방침</router-link>
          <router-link to="/terms-of-service" class="text-decoration-none text-muted">이용약관</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 1px solid #e5e5e5;
}

.footer h5 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.footer a {
  color: #6c757d;
}

.footer a:hover {
  color: #0d6efd;
}

.footer i {
  font-size: 1.25rem;
}
</style>