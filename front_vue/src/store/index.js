import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    // 用户信息
    user: JSON.parse(localStorage.getItem('user')) || null,
    // 是否登录
    isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
    // 当前布局
    layout: localStorage.getItem('userLayout') || 'BasicLayout',
    // 其他状态
    recipes: [],
    articles: [],
  },
  mutations: {
    // 设置用户信息
    setUser(state, user) {
      state.user = user;
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
      } else {
        localStorage.removeItem('user');
      }
    },
    // 设置登录状态
    setLoginStatus(state, status) {
      state.isLoggedIn = status;
      localStorage.setItem('isLoggedIn', status);
    },
    // 设置布局
    setLayout(state, layoutName) {
      state.layout = layoutName;
      localStorage.setItem('userLayout', layoutName);
    },
    // 设置食谱
    setRecipes(state, recipes) {
      state.recipes = recipes;
    },
    // 设置文章
    setArticles(state, articles) {
      state.articles = articles;
    },
  },
  actions: {
    // 登录操作
    login({ commit }, user) {
      commit('setUser', user);
      commit('setLoginStatus', true);
      const layoutType = user.calorie_version ? 'BasicLayout_calorie' : 'BasicLayout_cook';
      commit('setLayout', layoutType);
    },
    // 登出操作
    logout({ commit }) {
      commit('setUser', null);
      commit('setLoginStatus', false);
      commit('setLayout', 'BasicLayout');
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('user');
      localStorage.removeItem('userLayout');
    },
    // 初始化 Store
    async initializeStore({ commit }) {
      try {
        const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
        if (isLoggedIn) {
          const response = await axios.get('http://localhost:5000/users/user-info', {
            withCredentials: true,
          });
          const layoutType = response.data.calorie_version ? 'BasicLayout_calorie' : 'BasicLayout_cook';
          commit('setLayout', layoutType);
          commit('setLoginStatus', true);
          commit('setUser', response.data);
        } else {
          commit('setLayout', 'BasicLayout');
          commit('setLoginStatus', false);
        }
      } catch (error) {
        console.error('初始化 Store 失败:', error);
        commit('setLayout', 'BasicLayout');
        commit('setLoginStatus', false);
      }
    },
    // 检查登录状态
    async checkAuthStatus({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/users/user-info', {
          withCredentials: true,
        });
        commit('setUser', response.data);
        commit('setLoginStatus', true);
      } catch (error) {
        console.error('检查登录状态失败:', error);
        commit('setUser', null);
        commit('setLoginStatus', false);
      }
    },
  },
  getters: {
    // 获取登录状态
    isLoggedIn: (state) => state.isLoggedIn,
    // 获取当前布局
    currentLayout: (state) => state.layout,
    // 获取当前用户
    currentUser: (state) => state.user,
  },
});