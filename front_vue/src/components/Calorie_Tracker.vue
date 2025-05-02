<template>
  <div class="calorie-tracker">
    <a-form :model="localIntakeData" @finish="onRecordCalorieIntake" @finishFailed="onFinishFailed" class="form-section">
      <h3>记录卡路里摄入</h3>
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
          <a-form-item label="卡路里摄入 (大卡)" name="intake" :rules="[{ required: true, message: '请输入卡路里摄入！' }]">
            <a-input-number v-model:value="localIntakeData.intake" :min="0" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="用餐时间" name="meal_time" :rules="[{ required: true, message: '请输入用餐时间！' }]">
            <a-input v-model:value="localIntakeData.meal_time" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物项目" name="food_item" :rules="[{ required: true, message: '请输入食物项目！' }]">
            <a-input v-model:value="localIntakeData.food_item" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loading">记录</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
<<<<<<< Updated upstream
=======
import axios from 'axios';
>>>>>>> Stashed changes

const props = defineProps({
  intakeData: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
});

<<<<<<< Updated upstream
const emit = defineEmits(['record', 'finish-failed', 'update:intakeData']);

const localIntakeData = ref({ ...props.intakeData });

watch(() => props.intakeData, (newValue) => {
  localIntakeData.value = { ...newValue };
}, { deep: true });

watch(localIntakeData, (newValue) => {
  emit('update:intakeData', { ...newValue });
}, { deep: true });

const onRecordCalorieIntake = () => {
  emit('record', { ...localIntakeData.value });
=======
// 初始化 calculatorData，确保所有属性存在
const calculatorData = ref({
  food_name: '', // 初始化为字符串
  food_quantity: 1, // 初始化为数字
  meal_type: '早餐' // 初始化为默认值
});

const loadingIntake = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const calories = ref(null);
const recommendedRecipes = ref([]);
const loadingCalories = ref(false);

// 监听 calculatorData.food_name 的变化，并同步更新 intakeData.food_item
watch(
  () => calculatorData.value.food_name,
  (newValue) => {
    intakeData.value.food_item = newValue;
  }
);

const calculateCalories = async () => {
  loadingCalories.value = true;
  try {
    const response = await axios.post('http://localhost:5000/calorie/calculate', calculatorData.value, { withCredentials: true });
    calories.value = response.data.calories;
    recommendedRecipes.value = response.data.recommended_recipes;
    successMessage.value = '卡路里计算成功！';
    errorMessage.value = '';
    setTimeout(() => (successMessage.value = ''), 1000); // 1 秒后清除消息
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '卡路里计算失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loadingCalories.value = false;
  }
};

const recordCalorieIntake = async () => {
  loadingIntake.value = true;
  try {
    const response = await axios.post('http://localhost:5000/calorie/record_calorie_intake', {
      intake: intakeData.value.intake,
      meal_time: intakeData.value.meal_time,
      food_item: intakeData.value.food_item,
      food_quantity: calculatorData.value.food_quantity // 添加食物数量
    }, { withCredentials: true });
    successMessage.value = '卡路里摄入记录成功！';
    errorMessage.value = '';
    setTimeout(() => (successMessage.value = ''), 1000); // 1 秒后清除消息
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '记录卡路里摄入失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loadingIntake.value = false;
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
