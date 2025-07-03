import axios from '@/services/api'
import { useAuthStore } from '@/store/modules/authStore'


export const todoService = {
  async getTodos(page = 1, searchText = '', rowSize = 10) {
    const response = await axios.get('todos/todo_list', {
      params: {
        userId: useAuthStore().user?.userId || 0,
        page,
        row_size: rowSize,
        search_text: searchText
      }
    })
    return response.data
  },
  
  async getTodoById(id, params) {
    const response = await axios.get(`todos/todo_detail/${id}`, params)
    return response.data.todo_detail
  },
  
  async createTodo(todoData) {
    const response = await axios.post('todos/todo_insert', todoData)
    return response.data
  },
  
  async updateTodo(id, todoData) {
    const response = await axios.put(`todos/todo_update/${id}`, todoData)
    return response.data
  },
  
  async deleteTodo(id, params) {
    const response = await axios.delete(`todos/todo_delete/${id}`, params)
    return response.data
  },
  
  async toggleTodo(id, completed, params) {
    const response = await axios.patch(`todos/todo_toggle/${id}`, { completed }, params)
    return response.data
  }
}