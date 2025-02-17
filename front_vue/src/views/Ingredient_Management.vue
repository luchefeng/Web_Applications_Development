<template>
  <div class="ingredient-management">
    <a-tabs v-model:activeKey="activeKey">
      <a-tab-pane key="1" tab="食品柜">
        <ingredient-show ref="ingredientShowRef" />
      </a-tab-pane>
      <a-tab-pane key="2" tab="添加食材">
        <ingredient-add @ingredient-added="handleIngredientAdded" />
      </a-tab-pane>
      <a-tab-pane key="3" tab="推荐菜谱">
        <ingredient-recommend-recipes />
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import IngredientShow from '../components/Ingredient_Show.vue';
import IngredientAdd from '../components/Ingredient_Add.vue';
import IngredientRecommendRecipes from '../components/Ingredient_RecomendRecipes.vue';

const activeKey = ref('1');
const ingredientShowRef = ref(null);

const handleIngredientAdded = () => {
  // 刷新食品柜列表
  ingredientShowRef.value?.refreshList();
  // 切换到食品柜标签
  activeKey.value = '1';
};
</script>

<style scoped>
.ingredient-management {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}

.error {
  color: red;
}

.success {
  color: green;
}
</style>
