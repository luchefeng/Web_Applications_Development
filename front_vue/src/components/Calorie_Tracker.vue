<template>
  <div class="calorie-tracker">
    <a-form :model="localIntakeData" @finish="onRecordCalorieIntake" @finishFailed="onFinishFailed" class="form-section">
      <h3>记录卡路里摄入</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="卡路里摄入 (大卡)" name="intake" :rules="[{ required: true, message: '请输入卡路里摄入！' }]">
            <a-input-number v-model:value="localIntakeData.intake" :min="0" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="用餐时间" name="meal_time" :rules="[{ required: true, message: '请输入用餐时间！' }]">
            <a-input v-model:value="localIntakeData.meal_time" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物项目" name="food_item" :rules="[{ required: true, message: '请输入食物项目！' }]">
            <a-input v-model:value="localIntakeData.food_item" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loading">记录</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  intakeData: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['record', 'finish-failed', 'update:intakeData']);

const localIntakeData = ref({ ...props.intakeData });

watch(() => props.intakeData, (newValue) => {
  localIntakeData.value = { ...newValue };
}, { deep: true });

watch(localIntakeData, (newValue) => {
  emit('update:intakeData', { ...newValue });
}, { deep: true });

const onRecordCalorieIntake = () => {
  emit('record', { ...localIntakeData.value });
};

const onFinishFailed = (errorInfo) => {
  emit('finish-failed', errorInfo);
};
</script>

<style scoped>
/* Add any specific styles here */
</style>
