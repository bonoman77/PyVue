import { defineStore } from 'pinia'
import { productService } from '@/services/productService'

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    currentProduct: null,
    currentPage: 1,
    totalPages: 0,
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchProducts(page = 1) {
      // 영상 목록 조회 로직
    },
    
    async fetchProductById(id) {
      // 영상 상세 조회 로직
    },
    
    setCurrentProduct(product) {
      // 현재 재생 중인 영상 설정
      this.currentProduct = product
    }
  }
})