<template>
  <div class="dashboard">
    <!-- 個人信息區塊 -->
    <section class="user-info">
      <h1 class="typewriter">欢迎，{{ user.username }}</h1>
    </section>

    <!-- 功能模塊區塊 -->
    <section class="feature-section">
      <a-row :gutter="[32, 32]" justify="center">
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
  padding: 20px 60px;  /* 增加整体内边距 */
  max-width: 1400px;
  margin: 0 auto;
}

.user-info {
  text-align: center;
  margin-bottom: 40px;  /* 增加底部间距 */
}

/* 增加字体粗细并修改打字机效果 */
.typewriter {
  overflow: hidden;
  border-right: .15em solid #42b983;
  white-space: nowrap;
  margin: 0 auto;
  letter-spacing: .15em;
  font-weight: 600;  /* 增加字体粗细 */
  font-size: 1.8em;  /* 适当增大字号 */
  animation: 
    typing 5s steps(40, end),      /* 增加动画时长从3.5s到5s */
    blink-caret .75s step-end infinite;
}

@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}

@keyframes blink-caret {
  from, to { border-color: transparent }
  50% { border-color: #42b983; }
}

.feature-section {
  margin: 40px 80px;  /* 增加section的外边距 */
  padding: 20px;      /* 添加内边距 */
}

.feature-section :deep(.ant-row) {
  margin: 0 -16px;    /* 调整卡片之间的间距 */
}

.feature-section :deep(.ant-card) {
  transition: transform 0.3s;
  margin-bottom: 0;
}

.feature-section :deep(.ant-card-cover) {
  height: 180px; /* 减小图片高度 */
  overflow: hidden;
}

.feature-section :deep(.ant-card-cover img) {
  height: 100%;
  width: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.feature-section :deep(.ant-card:hover) {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.feature-section :deep(.ant-card:hover .ant-card-cover img) {
  transform: scale(1.05);
}

.feature-section :deep(.ant-card-meta-title) {
  font-size: 1.2em;
  margin-bottom: 8px;
}

.feature-section :deep(.ant-card-meta-description) {
  height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .dashboard {
    padding: 20px 40px;  /* 在较小屏幕上减小内边距 */
  }
  
  .feature-section {
    margin: 30px 40px;  /* 在较小屏幕上减小边距 */
  }
  
  .feature-section :deep(.ant-card-cover) {
    height: 160px;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 20px;
  }
  
  .feature-section {
    margin: 20px;
  }
  
  .feature-section :deep(.ant-card-cover) {
    height: 140px;
  }
}
</style>
