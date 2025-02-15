<template>
  <div class="calorie-management">
    <h2>卡路里管理</h2>

    <!-- 設置卡路里目標 -->
    <a-form :model="calorieData" @finish="calculateCalorieGoal" @finishFailed="onFinishFailed">
      <h3>設置卡路里目標</h3>
      <a-form-item label="性别" name="gender" :rules="[{ required: true, message: '請選擇您的性别！' }]">
        <a-select v-model:value="calorieData.gender">
          <a-select-option value="男">男</a-select-option>
          <a-select-option value="女">女</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item label="年龄" name="age" :rules="[{ required: true, message: '請輸入您的年龄！' }]">
        <a-input-number v-model:value="calorieData.age" :min="1" :max="120" />
      </a-form-item>
      <a-form-item label="身高 (cm)" name="height" :rules="[{ required: true, message: '請輸入您的身高！' }]">
        <a-input-number v-model:value="calorieData.height" :min="1" :max="300" :step="0.1" />
      </a-form-item>
      <a-form-item label="当前体重 (kg)" name="current_weight" :rules="[{ required: true, message: '請輸入您的当前体重！' }]">
        <a-input-number v-model:value="calorieData.current_weight" :min="1" :max="500" :step="0.1" />
      </a-form-item>
      <a-form-item label="目标体重 (kg)" name="target_weight" :rules="[{ required: true, message: '請輸入您的目标体重！' }]">
        <a-input-number v-model:value="calorieData.target_weight" :min="1" :max="500" :step="0.1" />
      </a-form-item>
      <a-form-item label="活动水平" name="activity_level" :rules="[{ required: true, message: '請選擇您的活动水平！' }]">
        <a-select v-model:value="calorieData.activity_level">
          <a-select-option value="久坐">久坐不動（很少或沒有運動）</a-select-option>
          <a-select-option value="轻度活动">輕度活動（輕鬆運動/運動1 - 3天/周）</a-select-option>
          <a-select-option value="中度活动">中度活動（中等運動/運動3 - 5天/周）</a-select-option>
          <a-select-option value="高度活动">高度活動（重度運動/運動6 - 7天/周）</a-select-option>
          <a-select-option value="极度活动">極度活動（非常重度運動/體力勞動）</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item label="减重时间 (天)" name="timeframe" :rules="[{ required: true, message: '請輸入减重时间！' }]">
        <a-input-number v-model:value="calorieData.timeframe" :min="1" :max="365" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">計算每日卡路里目标</a-button>
      </a-form-item>
    </a-form>

    <div v-if="calorieGoal !== null">
      <h3>每日卡路里目标: {{ calorieGoal }} 大卡</h3>
    </div>

    <!-- 卡路里攝入記錄 -->
    <a-form :model="intakeData" @finish="recordCalorieIntake" @finishFailed="onFinishFailed">
      <h3>記錄卡路里攝入</h3>
      <a-form-item label="卡路里攝入 (大卡)" name="intake" :rules="[{ required: true, message: '請輸入卡路里攝入！' }]">
        <a-input-number v-model:value="intakeData.intake" :min="0" :step="0.1" />
      </a-form-item>
      <a-form-item label="用餐時間" name="meal_time" :rules="[{ required: true, message: '請輸入用餐時間！' }]">
        <a-input v-model:value="intakeData.meal_time" />
      </a-form-item>
      <a-form-item label="食物項目" name="food_item" :rules="[{ required: true, message: '請輸入食物項目！' }]">
        <a-input v-model:value="intakeData.food_item" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">記錄</a-button>
      </a-form-item>
    </a-form>

    <!-- 體重記錄 -->
    <a-form :model="weightData" @finish="recordWeight" @finishFailed="onFinishFailed">
      <h3>記錄體重</h3>
      <a-form-item label="體重 (kg)" name="weight" :rules="[{ required: true, message: '請輸入體重！' }]">
        <a-input-number v-model:value="weightData.weight" :min="0" :step="0.1" />
      </a-form-item>
      <a-form-item label="日期" name="date" :rules="[{ required: true, message: '請選擇日期！' }]">
        <a-date-picker v-model:value="weightData.date" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">記錄</a-button>
      </a-form-item>
    </a-form>

    <!-- 科普欄 -->
    <section class="science-section">
      <h3>科普欄</h3>
      <p>卡路里（Calorie）是衡量食物能量的單位。1 卡路里相當於 1 克水溫度升高 1 攝氏度所需的能量。在我們日常飲食中，卡路里的攝入和消耗對於維持體重和健康非常重要。</p>
      <ul>
        <li><strong>基礎代謝率（BMR）:</strong> 基礎代謝率是指在靜止狀態下，身體維持基本生理功能所需的能量。</li>
        <li><strong>總能量消耗（TDEE）:</strong> 總能量消耗是指每天通過各種活動（包括運動和日常活動）所消耗的總能量。</li>
        <li><strong>健康飲食:</strong> 建議飲食中包含均衡的蛋白質、碳水化合物和脂肪，並注重攝取維生素和礦物質。</li>
      </ul>
    </section>

    <!-- 錯誤和成功消息 -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const calorieData = ref({
  gender: '男',
  age: 25,
  height: 175,
  current_weight: 70,
  target_weight: 65,
  activity_level: '中度活動',
  timeframe: 60
});

const intakeData = ref({
  intake: '',
  meal_time: '',
  food_item: ''
});

const weightData = ref({
  weight: '',
  date: ''
});

const calorieGoal = ref(null);
const errorMessage = ref('');
const successMessage = ref('');

const calculateCalorieGoal = async () => {
  try {
    console.log('Sending data to backend:', calorieData.value);
    const response = await axios.post('http://localhost:5000/calorie/set_calorie_goal', calorieData.value, { withCredentials: true });
    console.log('Response from backend:', response.data);
    calorieGoal.value = response.data.data.daily_calorie_goal;
    successMessage.value = '卡路里目標計算成功！';
    errorMessage.value = '';
  } catch (error) {
    console.error('Failed to set calorie goal:', error);
    console.error('Error response data:', error.response?.data);
    errorMessage.value = error.response?.data?.message || '計算卡路里目標失敗，請稍後再試。';
    successMessage.value = '';
  }
};

const recordCalorieIntake = async () => {
  try {
    const response = await axios.post('http://localhost:5000/calorie/record_calorie_intake', intakeData.value, { withCredentials: true });
    console.log('Calorie intake record response:', response.data);
    successMessage.value = '卡路里攝入記錄成功！';
    errorMessage.value = '';
  } catch (error) {
    console.error('Failed to record calorie intake:', error);
    console.error('Error response data:', error.response?.data);
    errorMessage.value = error.response?.data?.message || '記錄卡路里攝入失敗，請稍後再試。';
    successMessage.value = '';
  }
};

const recordWeight = async () => {
  try {
    const formattedDate = weightData.value.date.format('YYYY-MM-DD');
    const data = {
      ...weightData.value,
      date: formattedDate
    };
    const response = await axios.post('http://localhost:5000/calorie/record_weight', data, { withCredentials: true });
    console.log('Weight record response:', response.data);
    successMessage.value = '體重記錄成功！';
    errorMessage.value = '';
  } catch (error) {
    console.error('Failed to record weight:', error);
    console.error('Error response data:', error.response?.data);
    errorMessage.value = error.response?.data?.message || '記錄體重失敗，請稍後再試。';
    successMessage.value = '';
  }
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};
</script>

<style scoped>
.calorie-management {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.error {
  color: red;
}

.success {
  color: green;
}

.science-section {
  margin-top: 20px;
}

.science-section h3 {
  color: #42b983;
  margin-bottom: 10px;
}

.science-section p {
  margin-bottom: 10px;
}

.science-section ul {
  list-style: none;

  padding: 0;
}

.science-section ul li {
  margin: 10px 0;
  padding-left: 20px;
  position: relative;
}

.science-section ul li:before {
  content: "•";
  color: #42b983;
  position: absolute;
  left: 0;
}
</style>
