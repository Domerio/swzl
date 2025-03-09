// frontend/src/router/index.js
import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'

Vue.use(VueRouter)

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login/index.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/student-dashboard',
        name: 'StudentDashboard',
        component: () => import('@/views/Dashboard/StudentDashboard.vue'),
        meta: { 
            requiresAuth: true,
            role: 'student'
        }
    },
    {
        path: '/staff-dashboard',
        name: 'StaffDashboard',
        component: () => import('@/views/Dashboard/StaffDashboard.vue'),
        meta: { 
            requiresAuth: true,
            role: 'staff'
        }
    },
    {
        path: '/admin-dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/Dashboard/AdminDashboard.vue'),
        meta: { 
            requiresAuth: true,
            role: 'admin'
        }
    },
    {
        path: '/',
        redirect: () => {
            if (store.getters.isAuthenticated && store.getters.userRole) {
                const roleRouteMap = {
                    student: '/student-dashboard',
                    staff: '/staff-dashboard',
                    admin: '/admin-dashboard'
                }
                return roleRouteMap[store.getters.userRole] || '/login'
            }
            return '/login'
        }
    },
    // 添加404路由
    {
        path: '*',
        redirect: '/'
    }
]

const router = new VueRouter({
    mode: 'history',
    base: '/',
    routes
})

// 添加路由错误处理
router.onError((error) => {
    console.error('Router error:', error)
    if (error.name === 'ChunkLoadError') {
        window.location.reload()
    }
})

router.beforeEach(async (to, from, next) => {
    try {
        // 检查用户认证状态
        const isAuthenticated = store.getters.isAuthenticated
        const userRole = store.getters.userRole

        // 如果路由需要认证
        if (to.matched.some(record => record.meta.requiresAuth)) {
            if (!isAuthenticated) {
                // 未登录，重定向到登录页
                next({
                    path: '/login',
                    query: { redirect: to.fullPath }
                })
            } else if (to.meta.role && to.meta.role !== userRole) {
                // 角色不匹配，重定向到对应的仪表板
                const roleRouteMap = {
                    student: '/student-dashboard',
                    staff: '/staff-dashboard',
                    admin: '/admin-dashboard'
                }
                next(roleRouteMap[userRole] || '/login')
            } else {
                // 认证通过且角色匹配
                next()
            }
        } else if (to.path === '/login' && isAuthenticated) {
            // 已登录用户访问登录页，重定向到对应的仪表板
            const roleRouteMap = {
                student: '/student-dashboard',
                staff: '/staff-dashboard',
                admin: '/admin-dashboard'
            }
            next(roleRouteMap[userRole] || '/')
        } else {
            // 不需要认证的路由
            next()
        }
    } catch (error) {
        console.error('Navigation error:', error)
        next('/login')
    }
})

export default router
