<template>
  <div class="article-detail">
    <h1>{{ article.title }}</h1>
    <p><strong>Author:</strong> {{ article.author }}</p>
    <p><strong>Published on:</strong> {{ article.publishedDate }}</p>
    <div v-html="article.content"></div>
    <router-link to="/articles">Back to Articles</router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      article: {}
    };
  },
  created() {
    this.fetchArticle();
  },
  methods: {
    async fetchArticle() {
      const articleId = this.$route.params.id;
      try {
        const response = await fetch(`http://localhost:5000/api/articles/${articleId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch article');
        }
        this.article = await response.json();
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.article-detail {
  padding: 20px;
}
.article-detail h1 {
  font-size: 2em;
}
.article-detail p {
  margin: 10px 0;
}
</style>