import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: () => import('../views/index.vue')
        },
        {
            path: '/todos',
            name: 'Todos',
            component: () => import('../views/todos/index.vue')
        }, 
        {
            path: '/todos/:todo_id',
            name: 'Todo',
            component: () => import('../views/todos/_id.vue')
        }, 
    ]
})

export default router; 
