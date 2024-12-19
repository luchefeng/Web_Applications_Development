<template>
  <div class="article-list">
    <h1>Articles</h1>
    <ul>
      <li v-for="article in articles" :key="article.id">
        <router-link :to="{ name: 'ArticleDetail', params: { id: article.id } }">
          {{ article.title }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      articles: []
    };
  },
  created() {
    this.fetchArticles();
  },
  methods: {
    async fetchArticles() {
      try {
        const response = await axios.get('/api/articles');
        this.articles = response.data;
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    }
  }
};
</script>

<style scoped>
.article-list {
  padding: 20px;
}
.article-list h1 {
  font-size: 2em;
}
.article-list ul {
  list-style-type: none;
  padding: 0;
}
.article-list li {
  margin: 10px 0;
}
</style>