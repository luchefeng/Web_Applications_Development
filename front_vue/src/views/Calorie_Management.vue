<template>
  <div class="calorie-management">
    <h2>卡路里管理</h2>

    <!-- 設置卡路里目標 -->
    <a-form :model="calorieData" @finish="calculateCalorieGoal" @finishFailed="onFinishFailed" class="form-section">
      <h3>設置卡路里目標</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="性别" name="gender" :rules="[{ required: true, message: '請選擇您的性别！' }]">
            <a-select v-model:value="calorieData.gender" style="width: 100%">
              <a-select-option value="男">男</a-select-option>
              <a-select-option value="女">女</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="年龄" name="age" :rules="[{ required: true, message: '請輸入您的年龄！' }]">
            <a-input-number v-model:value="calorieData.age" :min="1" :max="120" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="身高 (cm)" name="height" :rules="[{ required: true, message: '請輸入您的身高！' }]">
            <a-input-number v-model:value="calorieData.height" :min="1" :max="300" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="当前体重 (kg)" name="current_weight" :rules="[{ required: true, message: '請輸入您的当前体重！' }]">
            <a-input-number v-model:value="calorieData.current_weight" :min="1" :max="500" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="目标体重 (kg)" name="target_weight" :rules="[{ required: true, message: '請輸入您的目标体重！' }]">
            <a-input-number v-model:value="calorieData.target_weight" :min="1" :max="500" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="活动水平" name="activity_level" :rules="[{ required: true, message: '請選擇您的活动水平！' }]">
            <a-select v-model:value="calorieData.activity_level" style="width: 100%">
              <a-select-option value="久坐">久坐不動（很少或沒有運動）</a-select-option>
              <a-select-option value="轻度活动">輕度活動（輕鬆運動/運動1 - 3天/周）</a-select-option>
              <a-select-option value="中度活动">中度活動（中等運動/運動3 - 5天/周）</a-select-option>
              <a-select-option value="高度活动">高度活動（重度運動/運動6 - 7天/周）</a-select-option>
              <a-select-option value="极度活动">極度活動（非常重度運動/體力勞動）</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="减重时间 (天)" name="timeframe" :rules="[{ required: true, message: '請輸入减重时间！' }]">
            <a-input-number v-model:value="calorieData.timeframe" :min="1" :max="365" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loadingCalorieGoal">計算每日卡路里目标</a-button>
      </a-form-item>
    </a-form>

    <!-- 顯示卡路里目標 -->
    <div v-if="calorieGoal !== null" class="result-section">
      <h3>每日卡路里目标: {{ calorieGoal }} 大卡</h3>
    </div>

    <!-- 卡路里計算器 -->
    <a-form :model="calculatorData" @finish="calculateCalories" @finishFailed="onFinishFailed" class="form-section">
      <h3>卡路里計算器</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物名稱" name="food_name" :rules="[{ required: true, message: '請輸入食物名稱！' }]">
            <a-input v-model:value="calculatorData.food_name" placeholder="輸入食物名稱" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="食物數量 (克)" name="food_quantity" :rules="[{ required: true, message: '請輸入食物數量！' }]">
            <a-input-number v-model:value="calculatorData.food_quantity" :min="1" placeholder="輸入食物數量" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="選擇餐別" name="meal_type" :rules="[{ required: true, message: '請選擇餐別！' }]">
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
        <a-button type="primary" html-type="submit" :loading="loadingCalories">計算卡路里</a-button>
      </a-form-item>
    </a-form>

    <!-- 顯示卡路里計算結果 -->
    <div v-if="calories !== null" class="result-section">
      <h3>卡路里計算結果: {{ calories }} 大卡</h3>
      <p>提醒：實際情況會有所波動，請以現品為準。</p>
      <h3>推薦菜譜</h3>
      <ul>
        <li v-for="recipe in recommendedRecipes" :key="recipe.id">{{ recipe.name }}</li>
      </ul>
    </div>

    <!-- 卡路里攝入記錄 -->
    <a-form :model="intakeData" @finish="recordCalorieIntake" @finishFailed="onFinishFailed" class="form-section">
      <h3>記錄卡路里攝入</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="卡路里攝入 (大卡)" name="intake" :rules="[{ required: true, message: '請輸入卡路里攝入！' }]">
            <a-input-number v-model:value="intakeData.intake" :min="0" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="用餐時間" name="meal_time" :rules="[{ required: true, message: '請輸入用餐時間！' }]">
            <a-input v-model:value="intakeData.meal_time" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物項目" name="food_item" :rules="[{ required: true, message: '請輸入食物項目！' }]">
            <a-input v-model:value="intakeData.food_item" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loadingIntake">記錄</a-button>
      </a-form-item>
    </a-form>

    <!-- 體重記錄 -->
    <a-form :model="weightData" @finish="recordWeight" @finishFailed="onFinishFailed" class="form-section">
      <h3>記錄體重</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="體重 (kg)" name="weight" :rules="[{ required: true, message: '請輸入體重！' }]">
            <a-input-number v-model:value="weightData.weight" :min="0" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="日期" name="date" :rules="[{ required: true, message: '請選擇日期！' }]">
            <a-date-picker v-model:value="weightData.date" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loadingWeight">記錄</a-button>
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
    <a-alert v-if="errorMessage" :message="errorMessage" type="error" show-icon class="alert-message" />
    <a-alert v-if="successMessage" :message="successMessage" type="success" show-icon class="alert-message" />
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
    successMessage.value = '卡路里目標計算成功！';
    errorMessage.value = '';
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '計算卡路里目標失敗，請稍後再試。';
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
    successMessage.value = '卡路里計算成功！';
    errorMessage.value = '';
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '卡路里計算失敗，請稍後再試。';
    successMessage.value = '';
  } finally {
    loadingCalories.value = false;
  }
};

const recordCalorieIntake = async () => {
  loadingIntake.value = true;
  try {
    const response = await axios.post('http://localhost:5000/calorie/record_calorie_intake', intakeData.value, { withCredentials: true });
    successMessage.value = '卡路里攝入記錄成功！';
    errorMessage.value = '';
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '記錄卡路里攝入失敗，請稍後再試。';
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
    successMessage.value = '體重記錄成功！';
    errorMessage.value = '';
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '記錄體重失敗，請稍後再試。';
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