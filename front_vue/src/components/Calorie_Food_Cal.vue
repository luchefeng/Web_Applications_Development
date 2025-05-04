<template>
  <div class="calorie-food-calculator">
    <a-form :model="localCalculatorData" @finish="onCalculateCalories" @finishFailed="onFinishFailed" class="form-section">
      <h3>卡路里计算器</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物名称" name="food_name" :rules="[{ required: true, message: '请输入食物名称！' }]">
            <a-input v-model:value="localCalculatorData.food_name" placeholder="输入食物名称" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="食物数量 (克)" name="food_quantity" :rules="[{ required: true, message: '请输入食物数量！' }]">
            <a-input-number v-model:value="localCalculatorData.food_quantity" :min="1" placeholder="输入食物数量" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="选择餐别" name="meal_type" :rules="[{ required: true, message: '请选择餐别！' }]">
            <a-select v-model:value="localCalculatorData.meal_type" style="width: 100%">
              <a-select-option value="早餐">早餐</a-select-option>
              <a-select-option value="午餐">午餐</a-select-option>
              <a-select-option value="晚餐">晚餐</a-select-option>
              <a-select-option value="其他">其他</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loading">计算卡路里</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
<<<<<<< Updated upstream
=======
import api from '../utils/api';  // 使用集中管理的API配置
>>>>>>> Stashed changes

const props = defineProps({
  calculatorData: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['calculate', 'finish-failed', 'update:calculatorData']);

<<<<<<< Updated upstream
const localCalculatorData = ref({ ...props.calculatorData });
=======
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
      const response = await api.get('/ingredient/search_usda', {
        params: { query: newName }
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
>>>>>>> Stashed changes

watch(() => props.calculatorData, (newValue) => {
  localCalculatorData.value = { ...newValue };
}, { deep: true });

watch(localCalculatorData, (newValue) => {
  emit('update:calculatorData', { ...newValue });
}, { deep: true });

<<<<<<< Updated upstream
const onCalculateCalories = () => {
  emit('calculate', { ...localCalculatorData.value });
=======
const calculateCalories = async () => {
  loadingCalories.value = true;
  try {
    // 使用已经计算好的总卡路里数据
    const data = {
      ...calculatorData.value,
      calories: calculatorData.value.total_calories
    };
    
    const response = await api.post('/calorie/calculate', data);
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
>>>>>>> Stashed changes
};

const onFinishFailed = (errorInfo) => {
  emit('finish-failed', errorInfo);
};
</script>

<style scoped>
/* Add any specific styles here */
</style>
