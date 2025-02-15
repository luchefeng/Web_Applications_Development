<template>
  <div class="calorie-management">
    <h2>卡路里管理</h2>

    <!-- 設置卡路里目標 -->
    <form @submit.prevent="calculateCalorieGoal">
      <h3>設置卡路里目標</h3>
      <div>
        <label for="gender">性别:</label>
        <select id="gender" v-model="calorieData.gender" required>
          <option value="男">男</option>
          <option value="女">女</option>
        </select>
      </div>
      <div>
        <label for="age">年龄:</label>
        <input type="number" id="age" v-model="calorieData.age" required />
      </div>
      <div>
        <label for="height">身高 (cm):</label>
        <input type="number" step="0.1" id="height" v-model="calorieData.height" required />
      </div>
      <div>
        <label for="current_weight">当前体重 (kg):</label>
        <input type="number" step="0.1" id="current_weight" v-model="calorieData.current_weight" required />
      </div>
      <div>
        <label for="target_weight">目标体重 (kg):</label>
        <input type="number" step="0.1" id="target_weight" v-model="calorieData.target_weight" required />
      </div>
      <div>
        <label for="activity_level">活动水平:</label>
        <select id="activity_level" v-model="calorieData.activity_level" required>
          <option value="久坐">久坐不動（很少或沒有運動）</option>
          <option value="轻度活动">輕度活動（輕鬆運動/運動1-3天/周）</option>
          <option value="中度活动">中度活動（中等運動/運動3-5天/周）</option>
          <option value="高度活动">高度活動（重度運動/運動6-7天/周）</option>
          <option value="极度活动">極度活動（非常重度運動/體力勞動）</option>
        </select>
      </div>
      <div>
        <label for="timeframe">减重时间 (天):</label>
        <input type="number" id="timeframe" v-model="calorieData.timeframe" required />
      </div>
      <button type="submit">計算每日卡路里目标</button>
    </form>

    <div v-if="calorieGoal !== null">
      <h3>每日卡路里目标: {{ calorieGoal }} 大卡</h3>
    </div>

    <!-- 卡路里攝入記錄 -->
    <form @submit.prevent="recordCalorieIntake">
      <h3>記錄卡路里攝入</h3>
      <div>
        <label for="intake">卡路里攝入 (大卡):</label>
        <input type="number" step="0.1" id="intake" v-model="intakeData.intake" required />
      </div>
      <div>
        <label for="meal_time">用餐時間:</label>
        <input type="text" id="meal_time" v-model="intakeData.meal_time" required />
      </div>
      <div>
        <label for="food_item">食物項目:</label>
        <input type="text" id="food_item" v-model="intakeData.food_item" required />
      </div>
      <button type="submit">記錄</button>
    </form>

    <!-- 體重記錄 -->
    <form @submit.prevent="recordWeight">
      <h3>記錄體重</h3>
      <div>
        <label for="weight">體重 (kg):</label>
        <input type="number" step="0.1" id="weight" v-model="weightData.weight" required />
      </div>
      <div>
        <label for="date">日期:</label>
        <input type="date" id="date" v-model="weightData.date" required />
      </div>
      <button type="submit">記錄</button>
    </form>

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

const calculateCalorieGoal = async () => {
  try {
    const response = await axios.post('http://localhost:5000/calorie/set_calorie_goal', calorieData.value, { withCredentials: true });
    calorieGoal.value = response.data.data.daily_calorie_goal;
    alert(response.data.message);
  } catch (error) {
    console.error('Failed to set calorie goal:', error);
    alert(error.response.data.message);
  }
};

const recordCalorieIntake = async () => {
  try {
    const response = await axios.post('http://localhost:5000/calorie/record_calorie_intake', intakeData.value, { withCredentials: true });
    alert(response.data.message);
  } catch (error) {
    console.error('Failed to record calorie intake:', error);
    alert(error.response.data.message);
  }
};

const recordWeight = async () => {
  try {
    const response = await axios.post('http://localhost:5000/calorie/record_weight', weightData.value, { withCredentials: true });
    alert(response.data.message);
  } catch (error) {
    console.error('Failed to record weight:', error);
    alert(error.response.data.message);
  }
};
</script>

<style scoped>
.calorie-management {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

form {
  display: flex;
  flex-direction: column;
}

form > div {
  margin-bottom: 10px;
}

form label {
  font-weight: bold;
}

form input, form select {
  padding: 8px;
  margin-top: 4px;
}

button {
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #369f79;
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
