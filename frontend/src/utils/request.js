import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // 修改API地址，移除多余的/api
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
    if(response.data?.status !== 'success') {
      return Promise.reject(new Error(response.data?.message))
    }
  },
  error => {
    console.error('Response error:', error)
    if (error.response.status === 401) {
      store.dispatch('logout')
      router.replace({ path: '/login', query: { redirect: router.currentRoute.fullPath } })
      // switch (error.response.status) {
      //   case 401:
      //     // 未授权，清除用户信息并跳转到登录页面
      //     store.dispatch('logout')
      //     router.replace({
      //       path: '/login',
      //       query: { redirect: router.currentRoute.fullPath }
      //     })
      //     Message.error('未授权，请重新登录')
      //     break
      //   case 403:
      //     Message.error('没有权限执行此操作')
      //     break
      //   case 404:
      //     Message.error('请求的资源不存在')
      //     break
      //   case 500:
      //     Message.error('服务器内部错误')
      //     break
      //   default:
      //     Message.error(error.response.data.error || '未知错误')
      // }
    } else {
      Message.error('网络错误，请检查您的网络连接')
    }
    return Promise.reject(error)
  }
)

export default service 