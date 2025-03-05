// frontend/src/router/index.js
import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/Login/LoginComponent.vue'
import Home from '@/views/Home/HomeComponent.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' }, // 默认跳转到登录页
  { path: '/login', name: 'Login', component: Login },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true } // 需要登录的页面标记
  }
]

const router = new VueRouter({
  mode: 'history', // 确保与 Django History模式配合
  base: process.env.BASE_URL,
  routes
})

// 路由守卫: 检查是否需要登录
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token') // 假设用 localStorage 存 token

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login') // 跳转登录页
  } else {
    next() // 放行
  }
})

export default router
