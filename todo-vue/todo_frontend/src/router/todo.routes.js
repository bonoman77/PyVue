import Todos from '@/pages/todo/index.vue'
import TodoDetail from '@/pages/todo/[id].vue'
import TodoWrite from '@/pages/todo/write.vue'

export const todoRoutes = [
  {
    path: '/todo',
    name: 'Todos',
    component: Todos
  },
  {
    path: '/todo/write',
    name: 'TodoWrite',
    component: TodoWrite
  },
  {
    path: '/todo/:id',
    name: 'TodoDetail',
    component: TodoDetail
  }
]