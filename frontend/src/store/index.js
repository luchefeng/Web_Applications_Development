import { createStore } from 'vuex';

export default createStore({
  state: {
    user: null,
    recipes: [],
    articles: [],
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
  },
  actions: {
    // 你的 actions
  },
  getters: {
    // 你的 getters
  },
});