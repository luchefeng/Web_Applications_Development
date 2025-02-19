import { createStore } from 'vuex';

export default createStore({
  state: {
    user: JSON.parse(localStorage.getItem('user')) || null,
    recipes: [],
    articles: [],
    isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
    layout: localStorage.getItem('userLayout') || 'BasicLayout' // 从localStorage读取布局
  },
  
  mutations: {
    setUser(state, user) {
      state.user = user;
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
      } else {
        localStorage.removeItem('user');
      }
    },
    setRecipes(state, recipes) {
      state.recipes = recipes;
    },
    setArticles(state, articles) {
      state.articles = articles;
    },
    setLoginStatus(state, status) {
      state.isLoggedIn = status;
      localStorage.setItem('isLoggedIn', status);
    },
    setLayout(state, layoutName) {
      state.layout = layoutName;
      localStorage.setItem('userLayout', layoutName); // 保存布局到localStorage
    }
  },
  
  actions: {
    login({ commit }, user) {
      commit('setUser', user);
      commit('setLoginStatus', true);
      // 根据用户版本设置布局
      const layoutType = user.calorie_version ? 'BasicLayout_calorie' : 'BasicLayout_cook';
      commit('setLayout', layoutType);
    },
    
    logout({ commit }) {
      commit('setUser', null);
      commit('setLoginStatus', false);
      commit('setLayout', 'BasicLayout');
      localStorage.removeItem('isLoggedIn');
    },
    
    async initializeStore({ commit }) {
      try {
        const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
        if (isLoggedIn) {
          const response = await axios.get('http://localhost:5000/users/user-info', {
            withCredentials: true
          });
          
          // 根据用户信息设置正确的布局
          const layoutType = response.data.calorie_version ? 'BasicLayout_calorie' : 'BasicLayout_cook';
          commit('setLayout', layoutType);
          commit('setLoginStatus', true);
          commit('setUser', response.data);
        } else {
          commit('setLayout', 'BasicLayout');
          commit('setLoginStatus', false);
        }
      } catch (error) {
        commit('setLayout', 'BasicLayout');
        commit('setLoginStatus', false);
      }
    },
    
    async checkAuthStatus({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/users/user-info', {
          withCredentials: true
        });
        commit('setUser', response.data);
        commit('setLoginStatus', true);
      } catch (error) {
        commit('setUser', null);
        commit('setLoginStatus', false);
      }
    }
  },
  
  getters: {
    isLoggedIn: state => state.isLoggedIn,
    currentLayout: state => state.layout,
    currentUser: state => state.user
  }
});