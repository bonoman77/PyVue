import axios from '@/services/api'
import { useAuthStore } from '@/store/modules/authStore'

export const boardService = {
  async getBoards(page = 1, searchText = '', rowSize = 10) {
    const response = await axios.get('boards/board_list', {
      params: {
        page,
        row_size: rowSize,
        search_text: searchText
      }
    })
    return response.data
  },
  
  async getBoardById(id) {
    const response = await axios.get(`boards/board_detail/${id}`)
    return response.data.board_detail
  },
  
  async createBoard(boardData) {
    const response = await axios.post('boards/board_insert', boardData)
    return response.data
  },
  
  async updateBoard(id, boardData) {
    const response = await axios.put(`boards/board_update/${id}`, boardData)
    return response.data
  },
  
  async deleteBoard(id, params) {
    const response = await axios.delete(`boards/board_delete/${id}`, params)
    return response.data
  },

  async displayBoard(id, display) {
    const response = await axios.patch(`boards/board_display/${id}`, {display})
    return response.data
  }
}