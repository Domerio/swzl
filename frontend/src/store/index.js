// frontend/src/store/index.js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || null,
    isAuthenticated: !!localStorage.getItem('token')
  },
  
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      state.isAuthenticated = !!token
      localStorage.setItem('token', token)
    },
    
    SET_USER(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    
    CLEAR_AUTH(state) {
      state.token = ''
      state.user = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
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
  },
  
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    userRole: state => state.user ? state.user.role : null,
    currentUser: state => state.user
  }
})
