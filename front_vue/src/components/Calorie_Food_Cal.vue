<template>
  <div class="calorie-food-calculator">
    <!-- 卡路里计算器 -->
    <a-form :model="calculatorData" @finish="calculateCalories" @finishFailed="onFinishFailed" class="form-section">
      <h3>卡路里计算器</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物名称" name="food_name" :rules="[{ required: true, message: '请输入食物名称！' }]">
            <a-input v-model:value="calculatorData.food_name" placeholder="输入食物名称" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="食物数量 (克)" name="food_quantity" :rules="[{ required: true, message: '请输入食物数量！' }]">
            <a-input-number v-model:value="calculatorData.food_quantity" :min="1" placeholder="输入食物数量" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      
      <!-- 添加单位卡路里显示 -->
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="单位卡路里 (kcal/100g)">
            <a-input-number v-model:value="calculatorData.unit_calories" disabled placeholder="自动计算" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="估计总卡路里 (kcal)">
            <a-input-number v-model:value="calculatorData.total_calories" disabled placeholder="自动计算" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loadingCalories">计算卡路里</a-button>
      </a-form-item>
    </a-form>

    <!-- 显示卡路里计算结果 -->
    <a-alert v-if="successMessage" :message="successMessage" type="success" show-icon closable class="alert-message" />
    <a-alert v-if="errorMessage" :message="errorMessage" type="error" show-icon closable class="alert-message" />
    <div v-if="calories !== null" class="result-section">
      <h3>卡路里计算结果: {{ calculatorData.total_calories }} 大卡</h3>
      <p>提醒：实际情况会有所波动，请以现品为准。</p>
      <h3>推荐菜谱</h3>
      <ul>
        <li v-for="recipe in recommendedRecipes" :key="recipe.id">{{ recipe.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

// 初始化 calculatorData，确保所有属性存在
const calculatorData = ref({
  food_name: '', // 初始化为字符串
  food_quantity: 1, // 初始化为数字
  meal_type: '早餐', // 初始化为默认值
  unit_calories: 0, // 单位卡路里 (kcal/100g)
  total_calories: 0 // 估计总卡路里
});

const calories = ref(null);
const recommendedRecipes = ref([]);
const errorMessage = ref('');
const successMessage = ref('');
const loadingCalories = ref(false);
let debounceTimer = null;

// 监听食物名称变化，获取单位卡路里
watch(() => calculatorData.value.food_name, (newName) => {
  clearTimeout(debounceTimer);
  
  if (!newName || newName.trim() === '') {
    calculatorData.value.unit_calories = 0;
    calculatorData.value.total_calories = 0;
    return;
  }
  
  debounceTimer = setTimeout(async () => {
    try {
      loadingCalories.value = true;
      const response = await axios.get('http://localhost:5000/ingredient/search_usda', {
        params: { query: newName },
        withCredentials: true
      });
      const data = response.data;
      calculatorData.value.unit_calories = data.unit_calories || 0;
      
      // 计算总卡路里
      updateTotalCalories();
    } catch (error) {
      console.error('Failed to fetch food calories:', error);
      errorMessage.value = '获取食物卡路里数据失败';
      setTimeout(() => (errorMessage.value = ''), 3000);
      calculatorData.value.unit_calories = 0;
    } finally {
      loadingCalories.value = false;
    }
  }, 500);
});

// 监听食物数量变化，更新总卡路里
watch(() => calculatorData.value.food_quantity, updateTotalCalories);

function updateTotalCalories() {
  if (calculatorData.value.unit_calories && calculatorData.value.food_quantity) {
    // 计算总卡路里: 食物数量(g) / 100 * 单位卡路里(kcal/100g)
    calculatorData.value.total_calories = Math.round(
      (calculatorData.value.food_quantity / 100) * calculatorData.value.unit_calories
    );
  } else {
    calculatorData.value.total_calories = 0;
  }
}

const calculateCalories = async () => {
  loadingCalories.value = true;
  try {
    // 使用已经计算好的总卡路里数据
    const data = {
      ...calculatorData.value,
      calories: calculatorData.value.total_calories
    };
    
    const response = await axios.post('http://localhost:5000/calorie/calculate', data, { withCredentials: true });
    calories.value = calculatorData.value.total_calories; // 确保显示的是表单中的总卡路里值
    recommendedRecipes.value = response.data.recommended_recipes;
    successMessage.value = '卡路里计算成功！';
    errorMessage.value = '';
    setTimeout(() => (successMessage.value = ''), 3000);
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '卡路里计算失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loadingCalories.value = false;
  }
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};
</script>

<style scoped>
.calorie-food-calculator {
  margin-bottom: 24px;
}

.result-section {
  margin-top: 16px;
}

.alert-message {
  margin-top: 16px;
}
</style>
