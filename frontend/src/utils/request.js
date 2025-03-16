import axios from 'axios'
import {Message} from 'element-ui'
import store from '@/store'
import router from '@/router'

// 创建axios实例
const service = axios.create({
    baseURL: 'http://127.0.0.1:8000/', // api的base_url
    timeout: 5000,    // 请求超时时间
    withCredentials: true  // 允许携带cookie
})

// 请求拦截器
service.interceptors.request.use(
    config => {
        // 从cookie中获取CSRF令牌
        const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1]
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken
        }

        // 如果存在token则添加到请求头
        const token = store.getters.token
        if (token) {
            config.headers['Authorization'] = `Token ${token}`
        }
        return config
    },
    error => {
        console.error('Request error:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    response => {
        if (response.headers['set-cookie']) {
            const csrfToken = response.headers['set-cookie'].find(c => c.startsWith('csrftoken='))
            if (csrfToken) {
                document.cookie = csrfToken
            }
        }
        // 检查响应数据是否存在且其状态是否为'success'
        if (response.data?.status !== 'success') {
            // 如果状态不是'success'，则返回一个被拒绝的Promise，并附带错误信息
            return Promise.reject(new Error(response.data?.message))
        }
        return response
    },
    error => {
        console.error('Response error:', error)
        if (error.response.status === 401) {
            store.dispatch('logout')
            router.replace({path: '/login', query: {redirect: router.currentRoute.fullPath}})
        } else {
            Message.error('网络错误，请检查您的网络连接')
        }
        return Promise.reject(error)
    }
)
// 创建axios实例
export default service