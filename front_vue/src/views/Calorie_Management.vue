<template>
  <div class="calorie-management">
    <h2>卡路里管理</h2>

    <!-- 显示全局错误和成功消息 -->
    <a-alert v-if="errorMessage" :message="errorMessage" type="error" show-icon class="alert-message" />
    <a-alert v-if="successMessage" :message="successMessage" type="success" show-icon class="alert-message" />

    <!-- 设置卡路里目标 -->
    <div name="calorie-goal" class="form-section">
      <calorie-goal-cal />
    </div>

    <!-- 卡路里计算器 -->
    <div name="calorie-cal" class="form-section">
      <calorie-food-cal />
    </div>

    <!-- 卡路里攝入記錄 -->
    <div name="calorie-tracker" class="form-section">
      <calorie-tracker />
    </div>


    <!-- 體重記錄 -->
    <div name="calorie-tracker" class="form-section">
      <calorie-weight-tracker />
    </div>

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
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import CalorieGoalCal from '../components/Calorie_Goal_Cal.vue'; // 确保路径正确
import CalorieFoodCal from '../components/Calorie_Food_Cal.vue'; // 确保路径正确
import CalorieTracker from "../components/Calorie_Tracker.vue"; // 确保路径正确
import CalorieWeightTracker from "../components/Calorie_Wei_Tracker.vue"; // 确保路径正确

const errorMessage = ref('');
const successMessage = ref('');
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