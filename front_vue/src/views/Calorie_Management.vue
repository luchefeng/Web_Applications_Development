<template>
  <div class="calorie-management">
    <h2>卡路里管理</h2>

    <!-- 设置卡路里目标 -->
    <a-form :model="calorieData" @finish="calculateCalorieGoal" @finishFailed="onFinishFailed" class="form-section">
      <h3>设置卡路里目标</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="性别" name="gender" :rules="[{ required: true, message: '请选择您的性别！' }]">
            <a-select v-model:value="calorieData.gender" style="width: 100%">
              <a-select-option value="男">男</a-select-option>
              <a-select-option value="女">女</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="年龄" name="age" :rules="[{ required: true, message: '请输入您的年龄！' }]">
            <a-input-number v-model:value="calorieData.age" :min="1" :max="120" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="身高 (cm)" name="height" :rules="[{ required: true, message: '请输入您的身高！' }]">
            <a-input-number v-model:value="calorieData.height" :min="1" :max="300" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="当前体重 (kg)" name="current_weight" :rules="[{ required: true, message: '请输入您的当前体重！' }]">
            <a-input-number v-model:value="calorieData.current_weight" :min="1" :max="500" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="目标体重 (kg)" name="target_weight" :rules="[{ required: true, message: '请输入您的目标体重！' }]">
            <a-input-number v-model:value="calorieData.target_weight" :min="1" :max="500" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="活动水平" name="activity_level" :rules="[{ required: true, message: '请选择您的活动水平！' }]">
            <a-select v-model:value="calorieData.activity_level" style="width: 100%">
              <a-select-option value="久坐">久坐不动（很少或没有运动）</a-select-option>
              <a-select-option value="轻度活动">轻度活动（轻松运动/运动1-3天/周）</a-select-option>
              <a-select-option value="中度活动">中度活动（中等运动/运动3-5天/周）</a-select-option>
              <a-select-option value="高度活动">高度活动（重度运动/运动6-7天/周）</a-select-option>
              <a-select-option value="极度活动">极度活动（非常重度运动/体力劳动）</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="减重时间 (天)" name="timeframe" :rules="[{ required: true, message: '请输入减重时间！' }]">
            <a-input-number v-model:value="calorieData.timeframe" :min="1" :max="365" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loadingCalorieGoal">计算每日卡路里目标</a-button>
      </a-form-item>
    </a-form>

    <!-- 顯示卡路里目標 -->
    <div v-if="calorieGoal !== null" class="result-section">
      <h3>每日卡路里目标: {{ calorieGoal.toFixed(2) }} 大卡</h3>
    </div>

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

    <!-- 顯示卡路里計算結果 -->
    <div v-if="calories !== null" class="result-section">
      <h3>卡路里计算结果: {{ calories }} 大卡</h3>
      <p>提醒：实际情况会有所波动，请以现品为准。</p>
      <h3>推荐菜谱</h3>
      <ul>
        <li v-for="recipe in recommendedRecipes" :key="recipe.id">{{ recipe.name }}</li>
      </ul>
    </div>

    <!-- 卡路里攝入記錄 -->
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
            <a-input v-model:value="intakeData.meal_time" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物项目" name="food_item" :rules="[{ required: true, message: '请输入食物项目！' }]">
            <a-input v-model:value="intakeData.food_item" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loadingIntake">记录</a-button>
      </a-form-item>
    </a-form>

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