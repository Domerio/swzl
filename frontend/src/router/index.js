import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login/LoginComponent.vue'),
    meta: {
      guestOnly: true // ▶新增meta标识，仅允许未登录访问
    }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home/HomeComponent.vue'), // ▶建议统一懒加载
    meta: {
      requiresAuth: true // ▶修正字段名（与守卫中的检查一致）
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL, // ▶当设置为history模式时，建议根据部署环境设置
  routes
})

// ▶优化后的全局路由守卫（解决重定向循环问题）
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')

  // 目标路由需要登录
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  }
  // 目标路由仅限未登录用户（如登录页）
  else if (to.matched.some(record => record.meta.guestOnly)) {
    if (isAuthenticated) {
      next({ path: '/home' })
    } else {
      next()
    }
  }
  // 其他情况放行
  else {
    next()
  }
})

// ▶保持重复导航的全局解决方案
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(() => {}) // ▲移除err参数
}

export default router
