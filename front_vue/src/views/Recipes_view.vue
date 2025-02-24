<template>
  <div class="recipes-container">
    <div class="recipes-header">
      <h2>菜谱列表</h2>
      <div class="header-controls">
        <a-input-search
          v-model:value="searchQuery"
          placeholder="搜索菜谱名称"
          style="width: 250px; margin-right: 16px;"
          @search="onSearch"
          @change="onSearch"
        />
        <a-button type="primary" @click="$router.push('/recipes/add')">
          添加新菜谱
        </a-button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <a-spin size="large" />
    </div>

    <div v-else-if="recipes.length === 0" class="empty-container">
      <a-empty description="暂无菜谱" />
    </div>

    <a-row :gutter="[16, 16]" v-else>
      <a-col :span="8" v-for="recipe in filteredRecipes" :key="recipe.id">
        <a-card hoverable class="recipe-card">
          <template #cover>
            <div class="recipe-cover">
              <h3>{{ recipe.title }}</h3>
            </div>
          </template>
          <a-card-meta>
            <template #title>
              {{ recipe.title }}
            </template>
            <template #description>
              <div class="recipe-ingredients">
                <strong>食材：</strong>
                <p>{{ getIngredientsSummary(recipe.ingredients) }}</p>
              </div>
              <div class="recipe-actions">
                <a-button type="primary" size="small" @click="showDetails(recipe)">
                  查看详情
                </a-button>
              </div>
            </template>
          </a-card-meta>
        </a-card>
      </a-col>
    </a-row>

    <!-- 菜谱详情弹窗 -->
    <a-modal
      v-model:visible="detailVisible"
      :title="selectedRecipe?.title"
      width="600px"
      @cancel="closeDetails"
      @ok="closeDetails"
    >
      <template v-if="selectedRecipe">
        <div class="recipe-detail">
          <h4>食材清单：</h4>
          <p>{{ formatIngredients(selectedRecipe.ingredients) }}</p>
          <h4>烹饪步骤：</h4>
          <p>{{ formatInstructions(selectedRecipe.instructions) }}</p>
        </div>
      </template>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';

const recipes = ref([]);
const loading = ref(true);
const detailVisible = ref(false);
const selectedRecipe = ref(null);
const searchQuery = ref('');

const getIngredientsSummary = (ingredients) => {
  const ingredientsList = ingredients.split('\n');
  const summary = ingredientsList.slice(0, 3).join(', ');
  return ingredientsList.length > 3 ? `${summary}...` : summary;
};

const formatIngredients = (ingredients) => {
  return ingredients.split('\n').join('\n');
};

const formatInstructions = (instructions) => {
  return instructions.split('\n').join('\n');
};

const showDetails = (recipe) => {
  selectedRecipe.value = recipe;
  detailVisible.value = true;
};

const closeDetails = () => {
  detailVisible.value = false;
  selectedRecipe.value = null;
};

const fetchRecipes = async () => {
  try {
    loading.value = true;
    const response = await axios.get('http://localhost:5000/recipes/list', {
      withCredentials: true
    });
    recipes.value = response.data;
  } catch (error) {
    console.error('Error fetching recipes:', error);
    message.error('获取菜谱列表失败');
  } finally {
    loading.value = false;
  }
};

const filteredRecipes = computed(() => {
  if (!searchQuery.value) {
    return recipes.value;
  }
  const query = searchQuery.value.toLowerCase();
  return recipes.value.filter(recipe => 
    recipe.title.toLowerCase().includes(query) ||
    recipe.ingredients.toLowerCase().includes(query)
  );
});

const onSearch = () => {
  // 实时搜索，不需要额外处理
  // 如果需要在输入完成后才搜索，可以在这里添加逻辑
};

onMounted(() => {
  fetchRecipes();
});
</script>

<style scoped>
.recipes-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.recipes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.recipes-header h2 {
  margin: 0;
  color: #42b983;
}

.header-controls {
  display: flex;
  align-items: center;
}

.recipe-card {
  height: 100%;
  transition: transform 0.3s;
}

.recipe-card:hover {
  transform: translateY(-5px);
}

.recipe-cover {
  height: 160px;
  background: linear-gradient(135deg, #42b983 0%, #3488aa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.recipe-cover h3 {
  color: white;
  text-align: center;
  margin: 0;
}

.recipe-ingredients {
  margin-bottom: 16px;
}

.recipe-actions {
  display: flex;
  justify-content: flex-end;
}

.loading-container, .empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.recipe-detail h4 {
  color: #42b983;
  margin-top: 16px;
}

.recipe-detail p {
  white-space: pre-line;
  margin: 8px 0;
}
</style>