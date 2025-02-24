<template>
  <div class="dashboard">
    <!-- 個人信息區塊 -->
    <section class="user-info">
      <h1>欢迎，{{ user.username }}</h1>
    </section>

    <!-- 功能模塊區塊 -->
    <section class="feature-section">
      <a-row justify="center">
        <a-col :span="16">
          <a-card hoverable @click="navigateTo('/ingredient-management')" class="feature-card">
            <template #cover>
              <img alt="ingredient management" src="../assets/ingredient-management.jpg" />
            </template>
            <a-card-meta title="食材管理" description="智能管理您的食材库，让烹饪更加便捷高效。" />
          </a-card>
        </a-col>
      </a-row>

      <a-row justify="center">
        <a-col :span="16">
          <a-card hoverable class="feature-card">
            <template #cover>
              <img alt="recipe recommendation" src="../assets/recipe-recommendation.jpg" />
            </template>
            <a-card-meta title="菜谱推荐" description="基于您的偏好和现有食材，智能推荐最适合的菜谱。" />
          </a-card>
        </a-col>
      </a-row>

      <a-row justify="center">
        <a-col :span="16">
          <a-card hoverable class="feature-card">
            <template #cover>
              <img alt="recipe browse" src="../assets/recipe-browse.jpg" />
            </template>
            <a-card-meta title="菜谱浏览与搜索" description="海量用户菜谱资源，便捷的搜索功能，助您轻松找到心仪的美食。" />
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

/* 修改打字机效果样式 */
.user-info h1 {  /* 修改选择器，确保只应用于 h1 标签 */
  overflow: hidden;
  border-right: .15em solid #42b983;
  white-space: nowrap;
  margin: 0 auto;
  letter-spacing: .15em;
  font-weight: 600;
  font-size: 1.8em;
  display: inline-block;  /* 添加这行 */
  animation: 
    typing 5s steps(40, end),
    blink-caret .75s step-end infinite;
}

@keyframes typing {
  from { 
    width: min-content;
    visibility: visible;  /* 确保文字始终可见 */
  }
  to { 
    width: max-content;
    visibility: visible;  /* 确保文字始终可见 */
  }
}

@keyframes blink-caret {
  from, to { border-color: transparent }
  50% { border-color: #42b983; }
}
</style>
