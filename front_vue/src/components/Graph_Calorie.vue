<template>
  <div class="graph-calorie">
    <h3>每日卡路里摄入统计</h3>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error">加载失败: {{ error }}</div>
    <div v-else-if="calorieData.length === 0">暂无卡路里数据记录</div>
    <template v-else>
      <a-slider 
        v-model:value="dateRange" 
        :min="0" 
        :max="Math.max(0, calorieData.length - 1)" 
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
const calorieData = ref([]);
const targetCalorie = ref(2000); // 默认目标卡路里
const dateRange = ref([0, 0]);
const loading = ref(true);
const error = ref('');
let chart = null;

const fetchCalorieData = async () => {
  loading.value = true;
  error.value = '';
  try {
    // 仅从用户信息端点获取目标卡路里
    try {
      const userResponse = await axios.get('http://localhost:5000/users/user-info', { withCredentials: true });
      if (userResponse.data && userResponse.data.calorie_goal) {
        targetCalorie.value = userResponse.data.calorie_goal;
        console.log('Fetched calorie goal from user profile:', targetCalorie.value);
      } else {
        // 如果用户信息中没有目标卡路里，保持默认值
        console.log('No calorie goal found in user profile, using default:', targetCalorie.value);
      }
    } catch (goalError) {
      console.error('Failed to fetch calorie goal:', goalError);
    }
    
    // 获取卡路里摄入记录
    const response = await axios.get('http://localhost:5000/calorie/intake_records', { withCredentials: true });
    if (response.data && Array.isArray(response.data.records)) {
      // 确保数据格式正确并处理任何异常日期格式
      calorieData.value = response.data.records.map(item => {
        return {
          date: formatDateString(item.date),
          intake: item.intake
        };
      });
      
      // 按日期排序数据
      calorieData.value.sort((a, b) => {
        return new Date(a.date) - new Date(b.date);
      });
      
      if (calorieData.value.length > 0) {
        dateRange.value = [0, calorieData.value.length - 1];
      }
    } else {
      calorieData.value = [];
      error.value = '获取数据格式不正确';
    }
  } catch (e) {
    console.error('Failed to fetch calorie data:', e);
    error.value = e.message || '获取卡路里数据失败';
  } finally {
    loading.value = false;
  }
};

// 确保日期格式一致，只保留年月日部分
const formatDateString = (dateStr) => {
  if (!dateStr) return '';
  
  // 如果包含时间部分，只保留日期部分
  if (dateStr.includes(' ') || dateStr.includes(':')) {
    const parts = dateStr.split(' ');
    return parts[0]; // 返回日期部分
  }
  
  return dateStr;
};

const filteredData = computed(() => {
  if (calorieData.value.length === 0) return [];
  return calorieData.value.slice(
    Math.min(dateRange.value[0], calorieData.value.length - 1), 
    Math.min(dateRange.value[1] + 1, calorieData.value.length)
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
  
  console.log('Target calorie value:', targetCalorie.value);
  
  const option = {
    title: {
      text: '每日卡路里摄入统计'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const date = params[0].name;
        const actualIntake = params[0].value;
        const targetIntake = params[1] ? params[1].value : targetCalorie.value;
        
        return `日期: ${date}<br/>
                实际摄入: ${actualIntake} 大卡<br/>
                目标摄入: ${targetIntake} 大卡`;
      }
    },
    legend: {
      data: ['每日摄入总量', '目标摄入']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%', // 增加底部间距，避免遮挡坐标轴
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: filteredData.value.map(item => item.date),
      axisLabel: {
        rotate: 45, // 旋转标签，防止重叠
        interval: 0,
        formatter: function(value) {
          // 清理日期格式，确保不显示时间部分
          return formatDateString(value);
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '卡路里 (大卡)'
    },
    series: [
      {
        name: '每日摄入总量',
        type: 'bar',
        data: filteredData.value.map(item => item.intake),
        itemStyle: {
          color: '#91cc75'
        }
      },
      {
        name: '目标摄入',
        type: 'line',
        data: Array(filteredData.value.length).fill(targetCalorie.value),
        lineStyle: {
          type: 'dashed',
          color: '#FF4500'
        },
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
  fetchCalorieData().then(() => {
    nextTick(() => {
      initChart();
    });
  });
});
</script>

<style scoped>
.graph-calorie {
  margin-bottom: 24px;
}
</style>
