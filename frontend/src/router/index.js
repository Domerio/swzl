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
        path: '/register',
        name: 'Register',
        meta: { requiresAuth: false },
        component: () => import('@/views/Login/index.vue')
    },
    {
        path: '/user-dashboard',
        name: 'UserDashboard',
        component: () => import('@/views/Dashboard/UserDashboard.vue'),
        meta: {
            requiresAuth: true,
            role: ['student', 'staff']
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
                    student: '/user-dashboard',
                    staff: '/user-dashboard',
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

        // 输出
        console.log('isAuthenticated:', isAuthenticated)
        console.log('userRole:', userRole)

        // 如果路由需要认证
        if (to.matched.some(record => record.meta.requiresAuth)) {
            if (!isAuthenticated) {
                // 未登录，重定向到登录页
                next({
                    path: '/login',
                    query: { redirect: to.fullPath }
                })
            } else {
                const allowedRoles = Array.isArray(to.meta.role) ? to.meta.role : [to.meta.role];
                if (!allowedRoles.includes(userRole)) {
                    // 角色不匹配，重定向到对应的仪表板
                    const roleRouteMap = {
                        student: '/user-dashboard',
                        staff: '/user-dashboard',
                        admin: '/admin-dashboard'
                    }
                    const targetRoute = roleRouteMap[userRole] || '/login';
                    if (to.path !== targetRoute) {
                        next(targetRoute);
                    } else {
                        // 如果已经在目标路由，避免无限重定向
                        next(false);
                    }
                } else {
                    // 认证通过且角色匹配
                    next();
                }
            }
        } else if (to.path === '/login' && isAuthenticated) {
            // 已登录用户访问登录页，重定向到对应的仪表板
            const roleRouteMap = {
                student: '/user-dashboard',
                staff: '/user-dashboard',
                admin: '/admin-dashboard'
            }
            next(roleRouteMap[userRole] || '/');
        } else {
            // 不需要认证的路由
            next();
        }
    } catch (error) {
        console.error('Navigation error:', error)
        next('/login');
    }
})

export default router