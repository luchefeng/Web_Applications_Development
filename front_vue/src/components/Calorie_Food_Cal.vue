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
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loading">计算每日卡路里目标</a-button>
      </a-form-item>
    </a-form>

    <!-- 顯示卡路里目標 -->
    <div v-if="showCalorieGoal" class="result-section">
      <h3>每日卡路里目标: {{ Number(localCalorieGoal).toFixed(2) }} 大卡</h3>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  calorieData: {
    type: Object,
    required: true
  },
  calorieGoal: {
    type: [Number, String, null],
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['calculate', 'finish-failed', 'update:calorieData']);

// Create local refs to track form data
const localCalorieData = ref({ ...props.calorieData });
const localCalorieGoal = ref(props.calorieGoal);

// Watch for changes in props to update local data
watch(() => props.calorieData, (newValue) => {
  localCalorieData.value = { ...newValue };
}, { deep: true });

watch(() => props.calorieGoal, (newValue) => {
  localCalorieGoal.value = newValue;
});

// Computed property to determine if we should show the calorie goal
const showCalorieGoal = computed(() => {
  return localCalorieGoal.value !== null;
});

// Watch for local changes to emit updates
watch(localCalorieData, (newValue) => {
  emit('update:calorieData', { ...newValue });
}, { deep: true });

// Form submission handlers
const onCalculateCalorieGoal = () => {
  emit('calculate', { ...localCalorieData.value });
};

const onFinishFailed = (errorInfo) => {
  emit('finish-failed', errorInfo);
};
</script>

<style scoped>
.calorie-goal-calculator {
  margin-bottom: 24px;
}

.form-section {
  margin-bottom: 24px;
}

.result-section {
  margin-bottom: 24px;
}
</style>
