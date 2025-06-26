import axios from '@/services/api'

export const todoService = {
  async getTodos(page = 1, searchText = '', rowSize = 10) {
    const response = await axios.get('boards/todo_list', {
      params: {
        page,
        row_size: rowSize,
        search_text: searchText
      }
    })
    return response.data
  },
  
  async getTodoById(id) {
    const response = await axios.get(`boards/todo_detail/${id}`)
    return response.data.todo_detail
  },
  
  async createTodo(todoData) {
    const response = await axios.post('boards/todo_insert', todoData)
    return response.data
  },
  
  async updateTodo(id, todoData) {
    const response = await axios.put(`boards/todo_update/${id}`, todoData)
    return response.data
  },
  
  async deleteTodo(id) {
    const response = await axios.delete(`boards/todo_delete/${id}`)
    return response.data
  },
  
  async toggleTodo(id, completed) {
    const response = await axios.patch(`boards/todo_toggle/${id}`, { completed })
    return response.data
  }
}