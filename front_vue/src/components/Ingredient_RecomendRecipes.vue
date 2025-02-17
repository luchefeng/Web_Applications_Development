<template>
  <div class="recipe-recommend">
    <h2>为您推荐的菜谱</h2>
    <div class="filters">
      <a-form layout="inline">
        <a-form-item label="卡路里范围">
          <a-input-number 
            v-model:value="filters.minCalories" 
            :max="filters.maxCalories" 
            placeholder="最小值"
          />
          <span> - </span>
          <a-input-number 
            v-model:value="filters.maxCalories" 
            :min="filters.minCalories" 
            placeholder="最大值"
          />
        </a-form-item>
        <a-form-item label="使用现有食材">
          <a-switch v-model:checked="filters.useExistingOnly" />
        </a-form-item>
      </a-form>
    </div>

    <div class="waterfall-container">
      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :sm="12" :md="8" :lg="6" v-for="recipe in recommendedRecipes" :key="recipe.id">
          <a-card hoverable class="recipe-card">
            <template #cover>
              <img :alt="recipe.name" :src="recipe.image" />
            </template>
            <template #actions>
              <heart-outlined key="like" />
              <message-outlined key="comment" />
              <share-alt-outlined key="share" />
            </template>
            <a-card-meta :title="recipe.name">
              <template #description>
                <p>卡路里: {{ recipe.calories }}kcal</p>
                <p>所需食材: {{ recipe.ingredients.join(', ') }}</p>
                <a-tag v-if="recipe.matchRate" color="green">匹配度: {{ recipe.matchRate }}%</a-tag>
              </template>
            </a-card-meta>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { HeartOutlined, MessageOutlined, ShareAltOutlined } from '@ant-design/icons-vue';

// 筛选条件
const filters = ref({
  minCalories: 0,
  maxCalories: 1000,
  useExistingOnly: true
});

// 模拟数据
const recommendedRecipes = ref([
  {
    id: 1,
    name: '清炒白菜',
    calories: 120,
    ingredients: ['白菜', '蒜', '油'],
    image: '/path/to/image1.jpg',
    matchRate: 100
  },
  // ... 更多模拟数据
]);

// 后续需要实现的获取推荐菜谱方法
const fetchRecommendedRecipes = async () => {
  try {
    // TODO: 调用后端API获取推荐菜谱
  } catch (error) {
    console.error('Failed to fetch recommended recipes:', error);
  }
};

onMounted(() => {
  fetchRecommendedRecipes();
});
</script>

<style scoped>
.recipe-recommend {
  padding: 20px;
}

.filters {
  margin-bottom: 24px;
}

.waterfall-container {
  margin-top: 20px;
}

.recipe-card {
  margin-bottom: 16px;
  transition: transform 0.3s;
}

.recipe-card:hover {
  transform: translateY(-5px);
}

.recipe-card img {
  height: 200px;
  object-fit: cover;
}
</style>
