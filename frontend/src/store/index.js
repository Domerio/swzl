// frontend/src/store/index.js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: localStorage.getItem('token') || '',
        user: JSON.parse(localStorage.getItem('user')) || null,
        isAuthenticated: !!localStorage.getItem('token'),
        amapLoaded: false,
        amapInstance: null,
    },

    mutations: {
        SET_TOKEN(state, token) {
            state.token = token
            // state.isAuthenticated = !!token
            localStorage.setItem('token', token)
        },

        SET_USER(state, user) {
            state.user = user
            state.isAuthenticated = 'true'
            localStorage.setItem('user', JSON.stringify(user))
        },

        CLEAR_AUTH(state) {
            state.token = ''
            state.user = null
            state.isAuthenticated = false
            localStorage.removeItem('token')
            localStorage.removeItem('user')
        },

        SET_AMAP_LOADED: (state, status) => {
            state.amapLoaded = status
        },

        SET_AMAP_INSTANCE: (state, instance) => {
            state.amapInstance = instance
        }
    },

    actions: {
        login({ commit }, { token, user }) {
            commit('SET_TOKEN', token)
            commit('SET_USER', user)
        },

        logout({ commit }) {
            commit('CLEAR_AUTH')
        },

        async loadAMap({ commit }) {
            if (this.state.amapLoaded) return true;

            return new Promise((resolve, reject) => {
                window._AMapSecurityConfig = {
                    securityJsCode: "c684b8bc9a42d62c059edd9fee411dce"
                };

                const script = document.createElement('script')
                script.src = `https://webapi.amap.com/maps?v=2.0&key=3958565d98f73366bc8f766bcc44cb66&plugin=AMap.Geocoder,AMap.Scale,AMap.ToolBar`
                script.onload = () => {
                    commit('SET_AMAP_LOADED', true)
                    commit('SET_AMAP_INSTANCE', window.AMap)
                    resolve(true)
                }
                script.onerror = reject
                document.head.appendChild(script)
            })
        },
    },

    getters: {
        isAuthenticated: state => state.isAuthenticated,
        userRole: state => state.user ? state.user.role : null,
        currentUser: state => state.user
    }
})
