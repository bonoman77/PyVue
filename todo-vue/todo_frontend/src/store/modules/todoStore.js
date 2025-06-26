import { defineStore } from 'pinia'
import { todoService } from '@/services/todoService'

export const useTodoStore = defineStore('todo', {
  state: () => ({
    todos: [],
    currentTodo: null,
    currentPage: 1,
    totalPages: 0,
    rowSize: 10,
    searchText: '',
    loading: false,
    error: null
  }),
  
  getters: {
    getTodoById: (state) => (id) => {
      return state.todos.find(todo => todo.todo_id === id)
    }
  },
  
  actions: {
    async fetchTodos(page = this.currentPage, searchText = this.searchText) {
      this.loading = true
      this.error = null
      
      try {
        const data = await todoService.getTodos(page, searchText, this.rowSize)
        this.todos = data.todo_list
        this.totalPages = data.total_page
        this.currentPage = page
        this.searchText = searchText
      } catch (err) {
        this.error = err.message || '할 일 목록을 불러오는 데 실패했습니다.'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    
    async fetchTodoById(id) {
      this.loading = true
      this.error = null
      
      try {
        const todo = await todoService.getTodoById(id)
        this.currentTodo = todo
        return todo
      } catch (err) {
        this.error = err.message || '할 일 상세 정보를 불러오는 데 실패했습니다.'
        console.error(err)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async addTodo(todoData) {
      this.loading = true
      this.error = null
      
      try {
        await todoService.createTodo(todoData)
        await this.fetchTodos()
        return true
      } catch (err) {
        this.error = err.message || '할 일을 추가하는 데 실패했습니다.'
        console.error(err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    async updateTodo(id, todoData) {
      this.loading = true
      this.error = null
      
      try {
        await todoService.updateTodo(id, todoData)
        
        // 현재 상세 페이지에 있는 경우 현재 할 일 업데이트
        if (this.currentTodo && this.currentTodo.todo_id === id) {
          this.currentTodo = { ...this.currentTodo, ...todoData }
        }
        
        // 목록에 있는 할 일 업데이트
        const index = this.todos.findIndex(todo => todo.todo_id === id)
        if (index !== -1) {
          this.todos[index] = { ...this.todos[index], ...todoData }
        }
        
        return true
      } catch (err) {
        this.error = err.message || '할 일을 수정하는 데 실패했습니다.'
        console.error(err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    async deleteTodo(id) {
      this.loading = true
      this.error = null
      
      try {
        await todoService.deleteTodo(id)
        
        // 목록에서 삭제된 할 일 제거
        this.todos = this.todos.filter(todo => todo.todo_id !== id)
        
        // 현재 상세 페이지에 있는 경우 초기화
        if (this.currentTodo && this.currentTodo.todo_id === id) {
          this.currentTodo = null
        }
        
        return true
      } catch (err) {
        this.error = err.message || '할 일을 삭제하는 데 실패했습니다.'
        console.error(err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    async toggleTodo(id, completed) {
      this.error = null
      
      try {
        await todoService.toggleTodo(id, completed)
        
        // 목록에 있는 할 일 상태 업데이트
        const index = this.todos.findIndex(todo => todo.todo_id === id)
        if (index !== -1) {
          this.todos[index].completed = completed
        }
        
        // 현재 상세 페이지에 있는 경우 현재 할 일 업데이트
        if (this.currentTodo && this.currentTodo.todo_id === id) {
          this.currentTodo.completed = completed
        }
        
        return true
      } catch (err) {
        this.error = err.message || '할 일 상태 변경에 실패했습니다.'
        console.error(err)
        return false
      }
    },
    
    setSearchText(text) {
      this.searchText = text
      this.fetchTodos(1, text) // 검색 시 첫 페이지로 이동
    },
    
    resetState() {
      this.todos = []
      this.currentTodo = null
      this.currentPage = 1
      this.totalPages = 0
      this.searchText = ''
      this.loading = false
      this.error = null
    }
  }
})