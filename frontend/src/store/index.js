// frontend/src/store/index.js
import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";
import user from "@/store/modules/user";
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 安全的初始化结构
    user: {
      isAuthenticated: false,
      info: null       // { id: 1, username:'', real_name:'', role:'' }
    }
  },
  plugins: [createPersistedState({
    paths: ['user'] // 自动同步user模块到localStorage
  })],
  modules: { user },
  mutations: {
    // 用户登录成功回调
    LOGIN_SUCCESS(state, userData) {
      state.user.isAuthenticated = true
      state.user.info = userData
    },
    // 清除用户数据
    LOGOUT(state) {
      state.user.isAuthenticated = false
      state.user.info = null
    }
  },
  actions: {
    // 异步登录操作
    async login({ commit }, { username, password }) {
      try {
        const res = await axios.post('/api/login/', { username, password })
        commit('LOGIN_SUCCESS', res.data)  // 确保后端返回数据包含完整用户字段
        return Promise.resolve(res.data)
      } catch (error) {
        return Promise.reject(error)
      }
    }
  },
  getters: {
    currentUser: state => state.user.info
  }
})
