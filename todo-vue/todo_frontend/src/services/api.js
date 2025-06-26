import axios from 'axios'

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
        return config
    },
    error => Promise.reject(error)
)

// 응답 인터셉터
instance.interceptors.response.use(
    response => response,
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
