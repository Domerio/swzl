// frontend/src/router/index.js
import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/Login/LoginComponent.vue'
import store from '../store'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/login'
    }, // 默认跳转到登录页
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: {
            requiresAuth: false, // 登录页不需要认证
        }
    },
    {
        path: '/student/dashboard',
        component: () => import('@/views/StudentDashboard.vue'),
        meta: {
            requiresAuth: true,
            requiresRole: ['student'],
            allowCache: false // 禁用页面缓存
        },
        beforeEnter: (to, from, next) => {
            // 防止地址栏直接输入访问
            if (from.path === '/' && !store.state.user.isAuthenticated) {
                next('/login')
            } else {
                next()
            }
        }
    },
    {
        path: '/staff/dashboard',
        component: () => import('@/views/StaffDashboard.vue'),
        meta: {
            requiresAuth: true,
            requiresRole: ['staff']
        }
    },
    {
        path: '/admin/dashboard',
        component: () => import('@/views/AdminDashboard.vue'),
        meta: {
            requiresAuth: true,
            requiresRole: ['admin']
        }
    }
]

const router = new VueRouter({
    mode: 'history', // 确保与 Django History模式配合
    base: process.env.BASE_URL,
    routes,
})

router.beforeEach((to, from, next) => {
    // console.group(`路由守卫: ${from.path} → ${to.path}`)
    console.groupCollapsed(`路由守卫: ${from.path} → ${to.path}`)
    console.log('路由元信息:', JSON.parse(JSON.stringify(to.meta))) // 添加详细日志
    console.log('当前用户状态:', JSON.parse(JSON.stringify(store.state.user)))
    // 状态初始化逻辑
    if (!store.state.user._init) {
        const token = localStorage.getItem('token')
        const userData = JSON.parse(localStorage.getItem('userInfo') || '{}')
        store.commit('user/SET_INIT_STATE', {
            _init: true,
            ...userData,
            isAuthenticated: !!token
        })
    }
    console.log('[守卫验证] 当前角色:', store.state.user.role)
    console.log('[守卫验证] 目标路由权限要求:', to.meta.requiresRole)
    // 强制认证检查
    if (to.meta.requiresAuth) {
        if (!store.state.user.isAuthenticated) {
            console.warn('[守卫拦截] 未登录访问需认证路由')
            next({path: '/login', query: {redirect: to.fullPath}})
            return
        }
    }
    // 角色权限检查
    if (Array.isArray(to.meta.requiresRole) && to.meta.requiresRole.length > 0) {
        const normalizedUserRole = (store.state.user.role || '').trim().toLowerCase()
        const normalizedRequired = to.meta.requiresRole.map(r => r.trim().toLowerCase())

        const hasPermission = normalizedRequired.includes(normalizedUserRole)

        console.log('角色验证结果:',
            `用户角色[${normalizedUserRole}]`,
            `要求角色[${normalizedRequired}]`,
            `通过? ${hasPermission}`
        )

        if (!hasPermission) {
            Vue.prototype.$message.error(`你没有权限访问此页面，需要 ${to.meta.requiresRole.join('/')} 权限。`)
            return next({path: `/${normalizedUserRole}/dashboard` || '/'})
        }
    }
    next()
    console.groupEnd()
})
export default router
