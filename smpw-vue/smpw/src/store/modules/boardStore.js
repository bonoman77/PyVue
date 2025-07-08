import { defineStore } from 'pinia'
import { boardService } from '@/services/boardService'
import { useAuthStore } from '@/store/modules/authStore'

export const useBoardStore = defineStore('board', {
  state: () => ({
    boards: [],
    currentBoard: null,
    currentPage: 1,
    totalPages: 0,
    rowSize: 10,
    searchText: '',
    loading: false,
    error: null
  }),
  
  getters: {
    getBoardById: (state) => (id) => {
      return state.boards.find(board => board.board_id === id)
    }
  },
  
  actions: {
    async fetchBoards(page = this.currentPage, searchText = this.searchText) {
      // 게시글 목록 조회 로직
      this.loading = true
      this.error = null

      try {
        const data = await boardService.getBoards(page, searchText, this.rowSize)
        this.boards = data.board_list
        this.totalItems = data.total_cnt  // 전체 항목 수 저장
        this.totalPages = Math.ceil(data.total_cnt / this.rowSize)  // 전체 페이지 수 계산
        this.currentPage = page
        this.searchText = searchText
      } catch (err) {
        this.error = err.message || '게시글 목록을 불러오는 데 실패했습니다.'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    
    async fetchBoardById(id) {
      // 게시글 상세 조회 로직
      this.loading = true
      this.error = null
      
      try {
        const board = await boardService.getBoardById(id)
        this.currentBoard = board
        return board
      } catch (err) {
        this.error = err.message || '게시글 상세 정보를 불러오는 데 실패했습니다.'
        console.error(err)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async addBoard(boardData) {
      // 게시글 작성 로직
      this.loading = true
      this.error = null
      
      try {
        await boardService.createBoard(boardData)
        await this.fetchBoards()
        return true
      } catch (err) {
        this.error = err.message || '게시글을 추가하는 데 실패했습니다.'
        console.error(err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    async updateBoard(id, boardData) {
      // 게시글 수정 로직
      this.loading = true
      this.error = null
      
      try {
        await boardService.updateBoard(id, boardData)
        
        // 현재 상세 페이지에 있는 경우 현재 할 일 업데이트
        if (this.currentBoard && this.currentBoard.board_id === id) {
          this.currentBoard = { ...this.currentBoard, ...boardData }
        }
        
        // 목록에 있는 할 일 업데이트
        const index = this.boards.findIndex(board => board.board_id === id)
        if (index !== -1) {
          this.boards[index] = { ...this.boards[index], ...boardData }
        }
        
        return true
      } catch (err) {
        this.error = err.message || '게시글을 수정하는 데 실패했습니다.'
        console.error(err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    async deleteBoard(id) {
      // 게시글 삭제 로직
      this.loading = true
      this.error = null
      
      // authStore 인스턴스 생성
      const authStore = useAuthStore()
      
      try {
        await boardService.deleteBoard(id, { 
          params: { userId: authStore.user?.userId || 0 } 
        })
        
        // 목록에서 삭제된 할 일 제거
        this.boards = this.boards.filter(board => board.board_id !== id)
        
        // 현재 상세 페이지에 있는 경우 초기화
        if (this.currentBoard && this.currentBoard.board_id === id) {
          this.currentBoard = null
        }
        
        return true
      } catch (err) {
        this.error = err.message || '게시글을 삭제하는 데 실패했습니다.'
        console.error(err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    setSearchText(text) {
      this.searchText = text
      this.fetchBoards(1, text) // 검색 시 첫 페이지로 이동
    },
    
    async toggleDisplay(id, displayYn) {
      // 게시글 상태 변경 로직
      try {
        // authStore에서 userId 가져오기
        const authStore = useAuthStore()
        const userId = authStore.user?.userId || 0
        
        // userId를 params로 전달
        await boardService.displayBoard(id, displayYn)
        
        // 목록에 있는 할 일 상태 업데이트
        const index = this.boards.findIndex(board => Number(board.board_id) === Number(id))
        if (index !== -1) {
          this.boards[index].displayYn = displayYn
        }
        
        // 현재 상세 페이지에 있는 경우 현재 할 일 업데이트
        if (this.currentBoard && Number(this.currentBoard.board_id) === Number(id)) {
          this.currentBoard.displayYn = displayYn
        }
        
        return true
      } catch (error) {
        console.error('게시글 상태 변경 실패:', error)
        return false
      }
    },
    
    resetState() {
      this.boards = []
      this.currentBoard = null
      this.currentPage = 1
      this.totalPages = 0
      this.searchText = ''
      this.loading = false
      this.error = null
    }
  }
})