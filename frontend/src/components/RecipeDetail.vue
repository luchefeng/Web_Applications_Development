<template>
  <div class="recipe-detail">
    <h1>{{ recipe.title }}</h1>
    <img :src="recipe.image" alt="Recipe Image" />
    <h2>Ingredients</h2>
    <ul>
      <li v-for="ingredient in recipe.ingredients" :key="ingredient">{{ ingredient }}</li>
    </ul>
    <h2>Instructions</h2>
    <p>{{ recipe.instructions }}</p>
    <button @click="goBack">Back to Recipes</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      recipe: {}
    };
  },
  created() {
    this.fetchRecipe();
  },
  methods: {
    async fetchRecipe() {
      const recipeId = this.$route.params.id;
      const response = await fetch(`http://localhost:5000/api/recipes/${recipeId}`);
      this.recipe = await response.json();
    },
    goBack() {
      this.$router.push({ name: 'Recipes' });
    }
  }
};
</script>

<style scoped>
.recipe-detail {
  padding: 20px;
}
.recipe-detail img {
  max-width: 100%;
  height: auto;
}
</style>