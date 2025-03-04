import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home/HomeComponent.vue'  // ▲关键路径验证▲

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/login'  // 确保根路径重定向正确
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login/LoginComponent.vue')
  },
  // ▲重点检查Home路由匹配段▲
  {
    path: '/home',       // 必须与跳转路径完全匹配
    name: 'Home',        // 确保与push调用名称一致
    component: Home,     // 或使用懒加载：() => import('@/views/Home.vue')
    meta: {
      requireAuth: true  // 如果启用路由守卫
    }
  }
]

const router = new VueRouter({
  mode: 'history',       // 重要检查点，需与后端配置配合
  base: process.env.BASE_URL,
  routes
})

// ▲全局路由守卫逻辑检查▲
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')

  // 对需要认证的路由进行拦截
  if (to.meta.requireAuth && !isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
