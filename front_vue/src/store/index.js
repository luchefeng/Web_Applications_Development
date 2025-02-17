import { createStore } from 'vuex';

export default createStore({
  state: {
    user: null,
    recipes: [],
    articles: [],
    isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setRecipes(state, recipes) {
      state.recipes = recipes;
    },
    setArticles(state, articles) {
      state.articles = articles;
    },
    setLoggedIn(state, value) {
      state.isLoggedIn = value;
      localStorage.setItem('isLoggedIn', value ? 'true' : 'false');
    },
  },
  actions: {
    // 你的 actions
  },
  getters: {
    // 你的 getters
  },
});