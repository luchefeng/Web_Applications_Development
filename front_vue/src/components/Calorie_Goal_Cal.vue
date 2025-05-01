<template>
  <div class="calorie-goal-calculator">
    <!-- 设置卡路里目标 -->
    <a-form :model="localCalorieData" @finish="onCalculateCalorieGoal" @finishFailed="onFinishFailed" class="form-section">
      <h3>设置卡路里目标</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="性别" name="gender" :rules="[{ required: true, message: '请选择您的性别！' }]">
            <a-select v-model:value="localCalorieData.gender" style="width: 100%">
              <a-select-option value="男">男</a-select-option>
              <a-select-option value="女">女</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="年龄" name="age" :rules="[{ required: true, message: '请输入您的年龄！' }]">
            <a-input-number v-model:value="localCalorieData.age" :min="1" :max="120" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="身高 (cm)" name="height" :rules="[{ required: true, message: '请输入您的身高！' }]">
            <a-input-number v-model:value="localCalorieData.height" :min="1" :max="300" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="当前体重 (kg)" name="current_weight" :rules="[{ required: true, message: '请输入您的当前体重！' }]">
            <a-input-number v-model:value="localCalorieData.current_weight" :min="1" :max="500" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="目标体重 (kg)" name="target_weight" :rules="[{ required: true, message: '请输入您的目标体重！' }]">
            <a-input-number v-model:value="localCalorieData.target_weight" :min="1" :max="500" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="活动水平" name="activity_level" :rules="[{ required: true, message: '请选择您的活动水平！' }]">
            <a-select v-model:value="localCalorieData.activity_level" style="width: 100%">
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
            <a-input-number v-model:value="localCalorieData.timeframe" :min="1" :max="365" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <!-- 根据表单现有的体重和身高自动计算BMI，实时显示结果 -->
          <a-form-item label="BMI (实时计算)">
            <a-input v-model:value="bmi" disabled style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loading">计算每日卡路里目标</a-button>
      </a-form-item>
    </a-form>

    <!-- 顯示卡路里目標 -->
    <div v-if="localCalorieGoal !== null" class="result-section">
      <h3>每日卡路里目标: {{ Number(localCalorieGoal).toFixed(2) }} 大卡</h3>
    </div>

    <a-alert v-if="successMessage" :message="successMessage" type="success" show-icon closable class="alert-message" />
    <a-alert v-if="errorMessage" :message="errorMessage" type="error" show-icon closable class="alert-message" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

const localCalorieData = ref({
  gender: '男',
  age: 25,
  height: 175,
  current_weight: 70,
  target_weight: 65,
  activity_level: '中度活动',
  timeframe: 60
});

const localCalorieGoal = ref(null);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const bmi = ref(''); // 用于实时显示 BMI

// 监听体重和身高的变化，实时计算 BMI
watch(
  () => [localCalorieData.value.height, localCalorieData.value.current_weight],
  ([height, weight]) => {
    if (height > 0 && weight > 0) {
      const heightInMeters = height / 100;
      bmi.value = (weight / (heightInMeters * heightInMeters)).toFixed(2);
    } else {
      bmi.value = '';
    }
  }
);

const onCalculateCalorieGoal = async () => {
  loading.value = true;
  try {
    const response = await axios.post('http://localhost:5000/calorie/set_calorie_goal', localCalorieData.value, { withCredentials: true });
    localCalorieGoal.value = response.data.data.daily_calorie_goal;
    successMessage.value = '卡路里目标计算成功！';
    errorMessage.value = '';
    setTimeout(() => (successMessage.value = ''), 1000); // 3 秒后清除消息
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '计算卡路里目标失败，请稍后再试。';
    successMessage.value = '';
  } finally {
    loading.value = false;
  }
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};
</script>

<style scoped>
.alert-message {
  margin-top: 16px;
}

.result-section {
  margin-top: 16px;
}
</style>
