import { createApp } from 'vue'
import { createHead } from '@vueuse/head'
import './styles/global.css'
import App from './App.vue'
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import router from './router';
import pinia from './store';

// PrimeVue 가져오기
import PrimeVue from 'primevue/config';

// Toast 옵션 설정
const toastOptions = {
  timeout: 2000, // 토스트 메시지 표시 시간을 2초로 설정 (기본값은 5초)
  position: "top-right"
};

const app = createApp(App);
const head = createHead();
app.use(head);
app.use(Toast, toastOptions);
app.use(router);
app.use(pinia);
app.use(PrimeVue, { ripple: true }); // PrimeVue 등록
app.mount('#app');
