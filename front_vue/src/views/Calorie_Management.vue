<template>
  <div class="calorie-management">
    <h2>卡路里管理</h2>

    <!-- 使用卡路里目标计算组件 -->
    <calorie-goal-cal 
      v-model:calorieData="calorieData"
      :calorieGoal="calorieGoal"
      :loading="loadingCalorieGoal"
      @calculate="calculateCalorieGoal"
      @finish-failed="onFinishFailed"
    />

<<<<<<< Updated upstream
    <!-- 卡路里计算器 -->
    <calorie-food-cal 
      v-model:calculatorData="calculatorData"
      :loading="loadingCalories"
      @calculate="calculateCalories"
      @finish-failed="onFinishFailed"
    />

    <!-- 顯示卡路里計算結果 -->
    <div v-if="calories !== null" class="result-section">
      <h3>卡路里计算结果: {{ calories }} 大卡</h3>
      <p>提醒：实际情况会有所波动，请以现品为准。</p>
      <h3>推荐菜谱</h3>
      <ul>
        <li v-for="recipe in recommendedRecipes" :key="recipe.id">{{ recipe.name }}</li>
      </ul>
    </div>

=======
>>>>>>> Stashed changes
    <!-- 卡路里攝入記錄 -->
    <calorie-tracker 
      v-model:intakeData="intakeData"
      :loading="loadingIntake"
      @record="recordCalorieIntake"
      @finish-failed="onFinishFailed"
    />

    <!-- 體重記錄 -->
    <calorie-weight-tracker 
      v-model:weightData="weightData"
      :loading="loadingWeight"
      @record="recordWeight"
      @finish-failed="onFinishFailed"
    />

    <!-- 科普栏 -->
    <section class="science-section">
      <h3>科普栏</h3>
      <p>卡路里（Calorie）是衡量食物能量的单位。1卡路里相当于1克水温度升高1摄氏度所需的能量。在我们日常饮食中，卡路里的摄入和消耗对于维持体重和健康非常重要。</p>
      <ul>
        <li><strong>基础代谢率（BMR）:</strong> 基础代谢率是指在静止状态下，身体维持基本生理功能所需的能量。</li>
        <li><strong>总能量消耗（TDEE）:</strong> 总能量消耗是指每天通过各种活动（包括运动和日常活动）所消耗的总能量。</li>
        <li><strong>健康饮食:</strong> 建议饮食中包含均衡的蛋白质、碳水化合物和脂肪，并注重摄取维生素和矿物质。</li>
      </ul>
    </section>

    <!-- 錯誤和成功消息 -->
    <a-alert v-if="errorMessage" :message="errorMessage" type="error" show-icon class="alert-message" />
    <a-alert v-if="successMessage" :message="successMessage" type="success" show-icon class="alert-message" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
<<<<<<< Updated upstream
import CalorieGoalCal from '@/components/Calorie_Goal_Cal.vue';
import CalorieFoodCal from '@/components/Calorie_Food_Cal.vue';
import CalorieTracker from '@/components/Calorie_Tracker.vue';
import CalorieWeightTracker from '@/components/Calorie_Weight_Tracker.vue';
=======
import CalorieGoalCal from '../components/Calorie_Goal_Cal.vue'; // 确保路径正确
import CalorieTracker from "../components/Calorie_Tracker.vue"; // 确保路径正确
import CalorieWeightTracker from "../components/Calorie_Wei_Tracker.vue"; // 确保路径正确
>>>>>>> Stashed changes

const calorieData = ref({
  gender: '男',
  age: 25,
  height: 175,
  current_weight: 70,
  target_weight: 65,
  activity_level: '中度活动',
  timeframe: 60
});

const calculatorData = ref({
  food_name: '',
  food_quantity: 1,
  meal_type: '早餐'
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
const calories = ref(null);
const recommendedRecipes = ref([]);
const errorMessage = ref('');
const successMessage = ref('');
const loadingCalorieGoal = ref(false);
const loadingCalories = ref(false);
const loadingIntake = ref(false);
const loadingWeight = ref(false);

const calculateCalorieGoal = async () => {
  loadingCalorieGoal.value = true;
  try {
    const response = await axios.post('http://localhost:5000/calorie/set_calorie_goal', calorieData.value, { withCredentials: true });
    calorieGoal.value = response.data.data.daily_calorie_goal;
    successMessage.value = '卡路里目标计算成功！';
    errorMessage.value = '';
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '计算卡路里目标失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loadingCalorieGoal.value = false;
  }
};

const calculateCalories = async () => {
  loadingCalories.value = true;
  try {
    const response = await axios.post('http://localhost:5000/calorie/calculate', calculatorData.value, { withCredentials: true });
    calories.value = response.data.calories;
    recommendedRecipes.value = response.data.recommended_recipes;
    successMessage.value = '卡路里计算成功！';
    errorMessage.value = '';
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
    const response = await axios.post('http://localhost:5000/calorie/record_calorie_intake', intakeData.value, { withCredentials: true });
    successMessage.value = '卡路里摄入记录成功！';
    errorMessage.value = '';
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '记录卡路里摄入失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loadingIntake.value = false;
  }
};

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
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '记录体重失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loadingWeight.value = false;
  }
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};
</script>

<style scoped>
.calorie-management {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.form-section {
  margin-bottom: 24px;
}

.result-section {
  margin-bottom: 24px;
}

.alert-message {
  margin-bottom: 16px;
}

.science-section {
  margin-top: 24px;
}

.science-section h3 {
  color: #42b983;
  margin-bottom: 16px;
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