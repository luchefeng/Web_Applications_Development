<template>
  <div class="recipes">
    <h1>Recipes</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <RecipeList :recipes="recipes" />
    </div>
    <button @click="fetchRecipes">Refresh Recipes</button>
  </div>
</template>

<script>
import RecipeList from '../components/RecipeList.vue';
import axios from 'axios';

export default {
  components: {
    RecipeList,
  },
  data() {
    return {
      recipes: [],
      loading: true,
    };
  },
  methods: {
    async fetchRecipes() {
      this.loading = true;
      try {
        const response = await axios.get('/api/recipes'); // Adjust the API endpoint as needed
        this.recipes = response.data;
      } catch (error) {
        console.error('Error fetching recipes:', error);
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchRecipes();
  },
};
</script>

<style scoped>
.recipes {
  padding: 20px;
}
</style>