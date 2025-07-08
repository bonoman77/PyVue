import axios from 'axios'
import { convertObjectKeysToCamelCase, convertObjectKeysToSnakeCase } from '@/utils/caseConverter'

const instance = axios.create({
    baseURL: 'http://localhost:4000/',
    timeout: 3000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 요청 인터셉터
instance.interceptors.request.use(
    config => {
        // 토큰이 있으면 헤더에 추가
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        
        // 요청 데이터의 키를 스네이크 케이스로 변환
        if (config.data) {
            config.data = convertObjectKeysToSnakeCase(config.data)
        }
        
        // params도 변환
        if (config.params) {
            config.params = convertObjectKeysToSnakeCase(config.params)
        }
        
        return config
    },
    error => Promise.reject(error)
)

// 응답 인터셉터
instance.interceptors.response.use(
    response => {
        // 응답 데이터의 키를 카멜 케이스로 변환
        if (response.data) {
            response.data = convertObjectKeysToCamelCase(response.data)
        }
        return response
    },
    error => {
        // 에러 처리 (401, 403 등)
        if (error.response?.status === 401) {
            // 인증 오류 처리
            localStorage.removeItem('token')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default instance
