import { createApp } from 'vue'
import './styles/global.css'
import App from './App.vue'
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import router from './router';
import pinia from './store';

const app = createApp(App);
app.use(Toast);
app.use(router);
app.use(pinia);
app.mount('#app');
