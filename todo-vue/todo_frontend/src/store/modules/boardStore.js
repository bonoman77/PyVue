import { defineStore } from 'pinia'
import { boardService } from '@/services/boardService'

export const useBoardStore = defineStore('board', {
  state: () => ({
    posts: [],
    currentPost: null,
    currentPage: 1,
    totalPages: 0,
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchPosts(page = 1) {
      // 게시글 목록 조회 로직
    },
    
    async fetchPostById(id) {
      // 게시글 상세 조회 로직
    },
    
    async createPost(post) {
      // 게시글 작성 로직
    },
    
    async updatePost(id, post) {
      // 게시글 수정 로직
    },
    
    async deletePost(id) {
      // 게시글 삭제 로직
    }
  }
})