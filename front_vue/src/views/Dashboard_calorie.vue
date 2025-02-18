<template>
    <div class="dashboard">
      <!-- 個人信息區塊 -->
      <section class="user-info">
        <h1>歡迎，{{ user.username }}</h1>
        <p><strong>用戶名：</strong> {{ user.username }}</p>
        <p><strong>電子郵件：</strong> {{ user.email }}</p>
      </section>
  
      <!-- 功能模塊區塊 -->
      <section class="feature-section">
        <a-row :gutter="[24, 24]" justify="center">
          <a-col :span="12">
            <a-card hoverable @click="navigateTo('/calorie-management')">
              <template #cover>
                <img alt="calorie management" src="../assets/calorie-management.jpg" />
              </template>
              <a-card-meta title="卡路里管理" description="科學計算每日攝入，合理規劃飲食計劃，幫助您實現健康飲食目標。" />
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card hoverable @click="navigateTo('/ingredient-management')">
              <template #cover>
                <img alt="ingredient management" src="../assets/ingredient-management.jpg" />
              </template>
              <a-card-meta title="食材管理" description="智能管理您的食材庫，讓烹飪更加便捷高效。" />
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card hoverable>
              <template #cover>
                <img alt="recipe recommendation" src="../assets/recipe-recommendation.jpg" />
              </template>
              <a-card-meta title="菜譜推薦" description="基於您的偏好和現有食材，智能推薦最適合的菜譜。" />
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card hoverable>
              <template #cover>
                <img alt="recipe browse" src="../assets/recipe-browse.jpg" />
              </template>
              <a-card-meta title="菜譜瀏覽與搜索" description="海量菜譜資源，便捷的搜索功能，助您輕鬆找到心儀的美食。" />
            </a-card>
          </a-col>
        </a-row>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const user = ref({
    username: '',
    email: ''
  });
  
  const router = useRouter();
  
  onMounted(async () => {
    try {
      const response = await axios.get('http://localhost:5000/users/user-info', { withCredentials: true });
      user.value = response.data;
    } catch (error) {
      console.error('Failed to fetch user info:', error);
    }
  });
  
  const navigateTo = (path) => {
    router.push(path);
  };
  </script>
  
  <style scoped>
  .dashboard {
    padding: 40px 20px;
  }
  
  .user-info {
    text-align: center;
    margin-bottom: 40px;
  }
  
  .feature-section {
    margin-top: 20px;
  }
  
  .feature-section .ant-card {
    transition: transform 0.3s;
  }
  
  .feature-section .ant-card:hover {
    transform: translateY(-5px);
    cursor: pointer;
  }
  </style>
  