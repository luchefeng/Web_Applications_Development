<template>
  <div class="articles">
    <h1>Articles</h1>
    <div v-if="loading">Loading articles...</div>
    <div v-else>
      <ul>
        <li v-for="article in articles" :key="article.id">
          <router-link :to="{ name: 'ArticleDetail', params: { id: article.id } }">
            {{ article.title }}
          </router-link>
        </li>
      </ul>
      <button @click="fetchArticles">Refresh Articles</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      articles: [],
      loading: true,
    };
  },
  methods: {
    async fetchArticles() {
      this.loading = true;
      try {
        const response = await axios.get('/api/articles');
        this.articles = response.data;
      } catch (error) {
        console.error('Error fetching articles:', error);
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchArticles();
  },
};
</script>

<style scoped>
.articles {
  padding: 20px;
}
</style>