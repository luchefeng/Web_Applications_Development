<template>
  <div class="recipe-list">
    <h2>Recipe Recommendations</h2>
    <div v-if="recipes.length === 0">
      <p>No recipes found. Please adjust your calorie intake or preferences.</p>
    </div>
    <ul>
      <li v-for="recipe in recipes" :key="recipe.id">
        <router-link :to="{ name: 'RecipeDetail', params: { id: recipe.id } }">
          {{ recipe.title }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
  name: 'RecipeList',
  setup() {
    const recipes = ref([]);

    const fetchRecipes = async () => {
      try {
        const response = await axios.get('/api/recipes'); // Adjust the API endpoint as needed
        recipes.value = response.data;
      } catch (error) {
        console.error('Error fetching recipes:', error);
      }
    };

    onMounted(fetchRecipes);

    return {
      recipes,
    };
  },
};
</script>

<style scoped>
.recipe-list {
  padding: 20px;
}
.recipe-list h2 {
  margin-bottom: 10px;
}
.recipe-list ul {
  list-style-type: none;
  padding: 0;
}
.recipe-list li {
  margin: 5px 0;
}
</style>