<template>
  <div class="calorie-tracker">
    <!-- 卡路里摄入记录 -->
    <a-form :model="intakeData" @finish="recordCalorieIntake" @finishFailed="onFinishFailed" class="form-section">
      <h3>记录卡路里摄入</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="卡路里摄入 (大卡)" name="intake" :rules="[{ required: true, message: '请输入卡路里摄入！' }]">
            <a-input-number v-model:value="intakeData.intake" :min="0" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="用餐时间" name="meal_time" :rules="[{ required: true, message: '请输入用餐时间！' }]">
            <a-input v-model:value="intakeData.meal_time" placeholder="输入用餐时间" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物项目" name="food_item" :rules="[{ required: true, message: '请输入食物项目！' }]">
            <a-input v-model:value="intakeData.food_item" placeholder="输入食物项目" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loadingIntake">记录</a-button>
      </a-form-item>
    </a-form>

    <!-- 显示成功或错误消息 -->
    <a-alert v-if="successMessage" :message="successMessage" type="success" show-icon closable class="alert-message" />
    <a-alert v-if="errorMessage" :message="errorMessage" type="error" show-icon closable class="alert-message" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

// 初始化 intakeData，确保所有属性存在
const intakeData = ref({
  intake: '', // 初始化为字符串或数字
  meal_time: '', // 初始化为字符串
  food_item: '' // 初始化为字符串
});

const loadingIntake = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const recordCalorieIntake = async () => {
  loadingIntake.value = true;
  try {
    const response = await axios.post('http://localhost:5000/calorie/record_calorie_intake', intakeData.value, { withCredentials: true });
    successMessage.value = '卡路里摄入记录成功！';
    errorMessage.value = '';
    setTimeout(() => (successMessage.value = ''), 1000); // 3 秒后清除消息
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '记录卡路里摄入失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loadingIntake.value = false;
  }
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};
</script>

<style scoped>
.calorie-tracker {
  margin-bottom: 24px;
}

.alert-message {
  margin-top: 16px;
}
</style>
