<template>
  <div class="calorie-food-calculator">
    <a-form :model="localCalculatorData" @finish="onCalculateCalories" @finishFailed="onFinishFailed" class="form-section">
      <h3>卡路里计算器</h3>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="食物名称" name="food_name" :rules="[{ required: true, message: '请输入食物名称！' }]">
            <a-input v-model:value="localCalculatorData.food_name" placeholder="输入食物名称" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="食物数量 (克)" name="food_quantity" :rules="[{ required: true, message: '请输入食物数量！' }]">
            <a-input-number v-model:value="localCalculatorData.food_quantity" :min="1" placeholder="输入食物数量" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="选择餐别" name="meal_type" :rules="[{ required: true, message: '请选择餐别！' }]">
            <a-select v-model:value="localCalculatorData.meal_type" style="width: 100%">
              <a-select-option value="早餐">早餐</a-select-option>
              <a-select-option value="午餐">午餐</a-select-option>
              <a-select-option value="晚餐">晚餐</a-select-option>
              <a-select-option value="其他">其他</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loading">计算卡路里</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  calculatorData: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['calculate', 'finish-failed', 'update:calculatorData']);

const localCalculatorData = ref({ ...props.calculatorData });

watch(() => props.calculatorData, (newValue) => {
  localCalculatorData.value = { ...newValue };
}, { deep: true });

watch(localCalculatorData, (newValue) => {
  emit('update:calculatorData', { ...newValue });
}, { deep: true });

const onCalculateCalories = () => {
  emit('calculate', { ...localCalculatorData.value });
};

const onFinishFailed = (errorInfo) => {
  emit('finish-failed', errorInfo);
};
</script>

<style scoped>
/* Add any specific styles here */
</style>
