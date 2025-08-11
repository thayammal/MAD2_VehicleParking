// store/index.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    token: localStorage.getItem('auth_token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null')
  },
  getters: {
    isAuthenticated: state => !!state.token,
    isAdmin: state => state.user?.role === 'admin',
    isUser: state => state.user?.role === 'user',
    authHeader: state => state.token ? { Authorization: `Bearer ${state.token}` } : {}
  },
  mutations: {
    SET_AUTH(state, { token, user }) {
      state.token = token
      state.user = user
      localStorage.setItem('auth_token', token)
      localStorage.setItem('user', JSON.stringify(user))
    },
    CLEAR_AUTH(state) {
      state.token = null
      state.user = null
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
    }
  },
  actions: {
    login({ commit }, { token, user }) {
      commit('SET_AUTH', { token, user })
    },
    logout({ commit }) {
      commit('CLEAR_AUTH')
    }
  }
})
