import axios from '@/services/api'

export const productService = {
  async getProducts(page = 1, searchText = '', rowSize = 10) {
    const response = await axios.get('products/product_list', {
      params: {
        page,
        row_size: rowSize,
        search_text: searchText
      }
    })
    return response.data
  },
  
  async getProductById(id) {
    const response = await axios.get(`products/product_detail/${id}`)
    return response.data.product_detail
  },
  
  async createProduct(productData) {
    const response = await axios.post('products/product_insert', productData)
    return response.data
  },
  
  async updateProduct(id, productData) {
    const response = await axios.put(`products/product_update/${id}`, productData)
    return response.data
  },
  
  async deleteProduct(id) {
    const response = await axios.delete(`products/product_delete/${id}`)
    return response.data
  },
}