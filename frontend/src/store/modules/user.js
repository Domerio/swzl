// frontend/src/store/modules/user.js
export default {
    namespaced: true,
    state: () => ({
        isAuthenticated: false,
        id: null,
        role: null,
        real_name: '未登录用户',
        phone: null,
        avatar: null,
    }),
    mutations: {
        SET_INIT_STATE(state, payload) {
            console.log('[Vuex Debug] SET_INIT_STATE payload:', payload)
            state.id = payload.id || null
            state.role = (payload.role || '').toLowerCase()
            state.real_name = payload.real_name || '未命名用户'
            state.isAuthenticated = Boolean(payload.isAuthenticated) // 强制转换布尔值
            state.phone = payload.phone || null
            state.avatar = payload.avatar || null
            state._init = payload._init !== false
        }
    },

}
