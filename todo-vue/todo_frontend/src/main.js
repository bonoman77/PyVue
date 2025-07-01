import { createApp } from 'vue'
import './styles/global.css'
import App from './App.vue'
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import router from './router';
import pinia from './store';

// Toast 옵션 설정
const toastOptions = {
  timeout: 2000, // 토스트 메시지 표시 시간을 2초로 설정 (기본값은 5초)
  position: "top-right"
};

const app = createApp(App);
app.use(Toast, toastOptions);
app.use(router);
app.use(pinia);
app.mount('#app');
