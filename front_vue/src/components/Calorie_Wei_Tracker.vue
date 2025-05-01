<template>
    <div class="calorie-weight-tracker">
    <!-- 體重記錄 -->
    <a-form :model="weightData" @finish="recordWeight" @finishFailed="onFinishFailed" class="form-section">
      <h3>记录体重</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="体重 (kg)" name="weight" :rules="[{ required: true, message: '请输入体重！' }]">
            <a-input-number v-model:value="weightData.weight" :min="0" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="日期" name="date" :rules="[{ required: true, message: '请选择日期！' }]">
            <a-date-picker v-model:value="weightData.date" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loadingWeight">记录</a-button>
      </a-form-item>
    </a-form>
    <a-alert v-if="successMessage" :message="successMessage" type="success" show-icon closable class="alert-message" />
    <a-alert v-if="errorMessage" :message="errorMessage" type="error" show-icon closable class="alert-message" />
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';


const weightData = ref({
  weight: '',
  date: ''
});

const errorMessage = ref('');
const successMessage = ref('');
const loadingWeight = ref(false);

const recordWeight = async () => {
  loadingWeight.value = true;
  try {
    const formattedDate = weightData.value.date.format('YYYY-MM-DD');
    const data = {
      ...weightData.value,
      date: formattedDate
    };
    const response = await axios.post('http://localhost:5000/calorie/record_weight', data, { withCredentials: true });
    successMessage.value = '体重记录成功！';
    errorMessage.value = '';
    setTimeout(() => (successMessage.value = ''), 1000); // 3 秒后清除消息
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '记录体重失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loadingWeight.value = false;
  }
};
</script>

<style scoped>
.alert-message {
  margin-top: 16px;
}
</style>
