<template>
  <div class="start-page">
    <!-- 第一个区块：版本选择 -->
    <section class="version-select">
      <h1 class="main-title animate__animated animate__fadeIn">
        选择适合您的版本
        <span class="subtitle">开启您的美食之旅</span>
      </h1>
      <a-row :gutter="[24, 24]" justify="center">
        <a-col :span="8" class="feature-list">
          <a-card hoverable @click="handleVersionSelect('calorie')">
            <a-card-meta title="卡路里管理版" description="适合需要控制饮食摄入的用户" />
            <template #cover>
              <ul>
                <li>食材管理</li>
                <li>菜谱推荐</li>
                <li>菜谱浏览</li>
                <li>卡路里管理</li>
              </ul>
            </template>
          </a-card>
        </a-col>
        <a-col :span="8" class="feature-list">
          <a-card hoverable @click="handleVersionSelect('basic')">
            <template #cover>
              <ul>
                <li>食材管理</li>
                <li>菜谱推荐</li>
                <li>菜谱浏览</li>
              </ul>
            </template>
            <a-card-meta title="仅美食管理版" description="适合想探索美食的用户" />
          </a-card>
        </a-col>
      </a-row>
    </section>

    <!-- 第二个区块：卡路里管理功能 -->
    <section class="feature-section" v-intersect="onIntersect">
      <a-row align="middle">
        <a-col :span="12" class="feature-text animate__animated" :class="{ 'animate__fadeInLeft': isVisible }">
          <h2>卡路里管理</h2>
          <p>科学计算每日摄入，合理规划饮食计划，帮助您实现健康饮食目标。</p>
          <ul>
            <li>每日卡路里追踪</li>
            <li>便捷卡路里计算</li>
            <li>贴心卡路里科普</li>
          </ul>
        </a-col>
        <a-col :span="12" class="animate__animated" :class="{ 'animate__fadeInRight': isVisible }">
          <img class="feature-image" src="../assets/calorie-management.jpg" alt="卡路里管理" />
        </a-col>
      </a-row>
    </section>

    <!-- 第三个区块：食材管理功能 -->
    <section class="feature-section alternate">
      <a-row align="middle">
        <a-col :span="12">
          <img class="feature-image" src="../assets/ingredient-management.jpg" alt="食材管理" />
        </a-col>
        <a-col :span="12" class="feature-text">
          <h2>食材管理</h2>
          <p>智能管理您的食材库，让烹饪更加便捷高效。</p>
          <ul>
            <li>食材库存追踪</li>
            <li>保质到期提醒</li>
            <li>单位热量展示</li>
          </ul>
        </a-col>
      </a-row>
    </section>

    <!-- 第四个区块：菜谱推荐功能 -->
    <section class="feature-section">
      <a-row align="middle">
        <a-col :span="12" class="feature-text">
          <h2>菜谱推荐</h2>
          <p>基于您的偏好和现有食材，智能推荐最适合的菜谱。</p>
          <ul>
            <li>个性化菜谱推荐</li>
            <li>基于食材库食材</li>
            <li>美味健康的搭配</li>
          </ul>
        </a-col>
        <a-col :span="12">
          <img class="feature-image" src="../assets/recipe-recommendation.jpg" alt="菜谱推荐" />
        </a-col>
      </a-row>
    </section>

    <!-- 第五个区块：菜谱浏览与搜索功能 -->
    <section class="feature-section alternate">
      <a-row align="middle">
        <a-col :span="12">
          <img class="feature-image" src="../assets/recipe-browse.jpg" alt="菜谱浏览" />
        </a-col>
        <a-col :span="12" class="feature-text">
          <h2>菜谱浏览与搜索</h2>
          <p>海量菜谱资源，便捷的搜索功能，助您轻松找到心仪的美食。</p>
          <ul>
            <li>多维度搜索筛选</li>
            <li>详细的烹饪步骤</li>
            <li>用户评价与分享</li>
          </ul>
        </a-col>
      </a-row>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import 'animate.css'; // 在脚本部分导入animate.css

const router = useRouter();
const isVisible = ref(false);

const onIntersect = (entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      isVisible.value = true;
    }
  });
};

const handleVersionSelect = (version) => {
  router.push({
    path: '/register',
    query: { version }
  });
};
</script>

<style scoped>

.start-page {
  padding: 40px 20px;
  font-family: 'Poppins', serif;
}

.main-title {
  text-align: center;
  margin-bottom: 40px;
  color: #42b983;
  font-size: 2.5em;
  position: relative;
  overflow: hidden;
  font-weight: 550;  /* 加粗 */
  /* text-shadow: 2px 2px 4px rgba(77, 95, 91, 0.2);  添加阴影 */
  letter-spacing: 2px;  /* 增加字间距提升可读性 */
}

.subtitle {
  display: block;
  font-size: 0.5em;
  color: #666;
  margin-top: 10px;
  font-family: 'Poppins', sans-serif;
  opacity: 0;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 0.5s;
  /* text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);  为副标题添加较淡的阴影 */
}

.feature-section {
  padding: 80px 20px;
  margin: 40px 0;
  transition: all 0.5s ease;
}

.feature-section:nth-child(even) {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.feature-text h2 {
  color: #42b983;
  margin-bottom: 20px;
  font-size: 2em;
  position: relative;
  padding-bottom: 15px;
}

/* 添加悬停效果 */
.feature-text h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: #42b983;
  transition: width 0.3s ease;
}

.feature-text:hover h2::after {
  width: 100px;
}

.feature-text p {
  font-size: 1.1em;
  line-height: 1.8;
  color: #666;
  margin-bottom: 25px;
}

.feature-text ul {
  list-style-type: none; /* 移除默认的列表标记 */
  padding: 0; /* 移除默认的内边距 */
}

.feature-text ul li {
  margin: 15px 0;
  padding-left: 30px;
  position: relative;
  transition: transform 0.3s ease;
}

.feature-text ul li:hover {
  transform: translateX(10px);
}

.feature-text ul li:before {
  content: "• ";
  color: #42b983;
  font-size: 1.5em;
  position: relative;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
}

.ant-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 15px;
  overflow: hidden;
}

.ant-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 功能区块图片样式 */
.feature-image {
  width: 100%;
  max-width: 500px;
  max-height: 300px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.feature-image:hover {
  transform: scale(1.02);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-title {
    font-size: 2em;
  }

  .feature-section {
    padding: 40px 20px;
  }

  .feature-text h2 {
    font-size: 1.5em;
  }

  .feature-image {
    max-width: 100%;
  }
}

.feature-list h2 {
  color: #42b983;
  margin-bottom: 20px;
  font-size: 2em;
  position: relative;
  padding-bottom: 15px;
}

/* 添加悬停效果 */
.feature-list h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: #42b983;
  transition: width 0.3s ease;
}

.feature-list:hover h2::after {
  width: 100px;
}

.feature-list p {
  font-size: 1.1em;
  line-height: 1.8;
  color: #666;
  margin-bottom: 25px;
}

.feature-list ul {
  list-style-type: none; /* 移除默认的列表标记 */
  padding: 0; /* 移除默认的内边距 */
}

.feature-list ul li {
  margin: 15px 0;
  padding-left: 30px;
  position: relative;
  transition: transform 0.3s ease;
}

.feature-list ul li:hover {
  transform: translateX(10px);
}

.feature-list ul li:before {
  content: "• ";
  color: #42b983;
  font-size: 1.5em;
  position: relative;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
}

</style>