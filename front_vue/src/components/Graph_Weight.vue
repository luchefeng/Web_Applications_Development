<template>
  <div class="graph-weight">
    <h3>体重记录</h3>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error">加载失败: {{ error }}</div>
    <div v-else-if="weightData.length === 0">暂无体重数据记录</div>
    <template v-else>
      <a-slider 
        v-model:value="dateRange" 
        :min="0" 
        :max="Math.max(0, weightData.length - 1)" 
        range 
        style="margin-bottom: 16px" 
      />
      <div ref="chartRef" style="width: 100%; height: 400px;"></div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';

const chartRef = ref(null);
const weightData = ref([]);
const dateRange = ref([0, 0]);
const loading = ref(true);
const error = ref('');
let chart = null;

const fetchWeightData = async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await axios.get('http://localhost:5000/calorie/weight_records', { withCredentials: true });
    if (response.data && Array.isArray(response.data.records)) {
      weightData.value = response.data.records;
      if (weightData.value.length > 0) {
        dateRange.value = [0, weightData.value.length - 1];
      }
    } else {
      weightData.value = [];
      error.value = '获取数据格式不正确';
    }
  } catch (e) {
    console.error('Failed to fetch weight data:', e);
    error.value = e.message || '获取体重数据失败';
  } finally {
    loading.value = false;
  }
};

const filteredData = computed(() => {
  if (weightData.value.length === 0) return [];
  return weightData.value.slice(
    Math.min(dateRange.value[0], weightData.value.length - 1), 
    Math.min(dateRange.value[1] + 1, weightData.value.length)
  );
});

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value);
    updateChart();
  }
};

const updateChart = () => {
  if (!chart || filteredData.value.length === 0) return;
  
  const option = {
    title: {
      text: '体重记录图表'
    },
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: filteredData.value.map(item => item.date)
    },
    yAxis: {
      type: 'value',
      name: '体重 (kg)'
    },
    series: [
      {
        name: '体重',
        type: 'line',
        data: filteredData.value.map(item => item.weight),
        smooth: true
      }
    ]
  };
  
  chart.setOption(option);
};

watch(filteredData, () => {
  nextTick(() => {
    updateChart();
  });
});

onMounted(() => {
  fetchWeightData().then(() => {
    nextTick(() => {
      initChart();
    });
  });
});
</script>

<style scoped>
.graph-weight {
  margin-bottom: 24px;
}
</style>
