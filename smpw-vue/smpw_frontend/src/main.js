import { createApp } from 'vue'
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css'
import './style.css'
import App from './App.vue'
import router from './router'

const options = {
    // 표시 시간(ms) - 예: 1000ms = 1초
    timeout: 2000
};

const app = createApp(App).use(Toast, options).use(router)

app.mount('#app')
