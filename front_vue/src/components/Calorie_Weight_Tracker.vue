<template>
  <div class="calorie-weight-tracker">
    <a-form :model="localWeightData" @finish="onRecordWeight" @finishFailed="onFinishFailed" class="form-section">
      <h3>记录体重</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="体重 (kg)" name="weight" :rules="[{ required: true, message: '请输入体重！' }]">
            <a-input-number v-model:value="localWeightData.weight" :min="0" :step="0.1" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="日期" name="date" :rules="[{ required: true, message: '请选择日期！' }]">
            <a-date-picker v-model:value="localWeightData.date" style="width: 100%" />
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
  weightData: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['record', 'finish-failed', 'update:weightData']);

const localWeightData = ref({ ...props.weightData });

watch(() => props.weightData, (newValue) => {
  localWeightData.value = { ...newValue };
}, { deep: true });

watch(localWeightData, (newValue) => {
  emit('update:weightData', { ...newValue });
}, { deep: true });

const onRecordWeight = () => {
  emit('record', { ...localWeightData.value });
};

const onFinishFailed = (errorInfo) => {
  emit('finish-failed', errorInfo);
};
</script>

<style scoped>
/* Add any specific styles here */
</style>
