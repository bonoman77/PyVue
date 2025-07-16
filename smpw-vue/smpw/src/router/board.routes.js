import BoardList from '@/pages/board/index.vue'
import BoardDetail from '@/pages/board/[id].vue'
import BoardWrite from '@/pages/board/write.vue'

export const boardRoutes = [
  {
    path: '/board',
    name: 'BoardList',
    component: BoardList,
    meta: { requiresAuth: true }
  },
  {
    path: '/board/write',
    name: 'BoardWrite',
    component: BoardWrite,
    meta: { requiresAuth: true }
  },
  {
    path: '/board/:id',
    name: 'BoardDetail',
    component: BoardDetail,
    meta: { requiresAuth: true }
  }
]