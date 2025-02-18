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
      <a-row justify="center">
        <a-col :span="16">
          <a-card hoverable @click="navigateTo('/ingredient-management')" class="feature-card">
            <template #cover>
              <img alt="ingredient management" src="../assets/ingredient-management.jpg" />
            </template>
            <a-card-meta title="食材管理" description="智能管理您的食材庫，讓烹飪更加便捷高效。" />
          </a-card>
        </a-col>
      </a-row>

      <a-row justify="center">
        <a-col :span="16">
          <a-card hoverable class="feature-card">
            <template #cover>
              <img alt="recipe recommendation" src="../assets/recipe-recommendation.jpg" />
            </template>
            <a-card-meta title="菜譜推薦" description="基於您的偏好和現有食材，智能推薦最適合的菜譜。" />
          </a-card>
        </a-col>
      </a-row>

      <a-row justify="center">
        <a-col :span="16">
          <a-card hoverable class="feature-card">
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

.feature-card {
  margin-bottom: 24px; /* 增加卡片之间的垂直间距 */
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  cursor: pointer;
}

/* 设置卡片图片高度统一 */
.feature-card :deep(.ant-card-cover img) {
  height: 50px;
  object-fit: cover;
}
</style>
