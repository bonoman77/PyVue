import Todos from '@/pages/todo/index.vue'
import TodoDetail from '@/pages/todo/[id].vue'
import TodoWrite from '@/pages/todo/write.vue'

export const todoRoutes = [
  {
    path: '/todo',
    name: 'Todos',
    component: Todos,
    meta: { requiresAuth: true }
  },
  {
    path: '/todo/write',
    name: 'TodoWrite',
    component: TodoWrite,
    meta: { requiresAuth: true }
  },
  {
    path: '/todo/:id',
    name: 'TodoDetail',
    component: TodoDetail,
    meta: { requiresAuth: true }
  }
]