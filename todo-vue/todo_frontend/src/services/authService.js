import axios from '@/services/api'

export const authService = {
  /**
   * 사용자 로그인
   * @param {Object} credentials - 로그인 정보 (username, password)
   * @returns {Promise<Object>} - 토큰과 사용자 정보
   */
  async login(credentials) {
    try {
      const response = await axios.post('/auth/login', credentials)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '로그인에 실패했습니다.')
    }
  },

  /**
   * 사용자 로그아웃
   * @returns {Promise<void>}
   */
  async logout() {
    try {
      // 서버에 로그아웃 요청 (토큰 무효화)
      await api.post('/auth/logout')
      // 로컬 스토리지에서 토큰 제거
      localStorage.removeItem('token')
    } catch (error) {
      console.error('로그아웃 중 오류 발생:', error)
      // 로컬에서는 항상 토큰을 제거
      localStorage.removeItem('token')
    }
  },

  /**
   * 현재 로그인한 사용자 정보 조회
   * @returns {Promise<Object>} - 사용자 정보
   */
  async getCurrentUser() {
    try {
      const response = await axios.get('/auth/me')
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '사용자 정보를 불러오는 데 실패했습니다.')
    }
  },

  /**
   * 새 사용자 등록
   * @param {Object} userData - 사용자 등록 정보 (username, password, email 등)
   * @returns {Promise<Object>} - 등록된 사용자 정보
   */
  async register(userData) {
    try {
      const response = await axios.post('/auth/register', userData)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '회원가입에 실패했습니다.')
    }
  },

  /**
   * 토큰 갱신
   * @returns {Promise<Object>} - 새 토큰
   */
  async refreshToken() {
    try {
      const response = await axios.post('/auth/refresh-token')
      const { token } = response.data
      localStorage.setItem('token', token)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '토큰 갱신에 실패했습니다.')
    }
  }
}