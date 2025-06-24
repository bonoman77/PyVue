import { createRouter, createWebHistory } from 'vue-router'; 
import Home from '@/pages/index.vue'
import Todos from '@/pages/todos/index.vue'
import Todo from '@/pages/todos/_id.vue'
import TodoCreate from '@/pages/todos/create/index.vue'

const  router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/todos',
      name: 'Todos',
      component: Todos
    },
    {
        path: '/todos/:todo_id',
        name: 'Todo',
        component: Todo
    }, 
    {
      path: '/todos/create',
      name: 'TodoCreate',
      component: TodoCreate
    }, 
  ]
})

export default router

