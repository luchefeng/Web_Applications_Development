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
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="选择餐别" name="meal_type" :rules="[{ required: true, message: '请选择餐别！' }]">
            <a-select v-model:value="calculatorData.meal_type" style="width: 100%">
              <a-select-option value="早餐">早餐</a-select-option>
              <a-select-option value="午餐">午餐</a-select-option>
              <a-select-option value="晚餐">晚餐</a-select-option>
              <a-select-option value="其他">其他</a-select-option>
            </a-select>
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
      <h3>卡路里计算结果: {{ calories }} 大卡</h3>
      <p>提醒：实际情况会有所波动，请以现品为准。</p>
      <h3>推荐菜谱</h3>
      <ul>
        <li v-for="recipe in recommendedRecipes" :key="recipe.id">{{ recipe.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

// 初始化 calculatorData，确保所有属性存在
const calculatorData = ref({
  food_name: '', // 初始化为字符串
  food_quantity: 1, // 初始化为数字
  meal_type: '早餐' // 初始化为默认值
});

const calories = ref(null);
const recommendedRecipes = ref([]);
const errorMessage = ref('');
const successMessage = ref('');
const loadingCalories = ref(false);

const calculateCalories = async () => {
  loadingCalories.value = true;
  try {
    const response = await axios.post('http://localhost:5000/calorie/calculate', calculatorData.value, { withCredentials: true });
    calories.value = response.data.calories;
    recommendedRecipes.value = response.data.recommended_recipes;
    successMessage.value = '卡路里计算成功！';
    errorMessage.value = '';
    setTimeout(() => (successMessage.value = ''), 1000); // 3 秒后清除消息
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
