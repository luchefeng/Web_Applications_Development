<template>
  <div class="start-page">
    <!-- 第一个区块：版本选择 -->
    <section class="version-select">
      <h1 class="main-title">选择适合您的版本</h1>
      <a-row :gutter="[24, 24]" justify="center">
        <a-col :span="8">
          <a-card hoverable @click="handleVersionSelect('calorie')">
            <template #cover>
              <img alt="calorie version" src="../assets/calorie-version.jpg" />
            </template>
            <a-card-meta title="卡路里管理版" description="适合需要控制饮食摄入的用户" />
          </a-card>
        </a-col>
        <a-col :span="8">
          <a-card hoverable @click="handleVersionSelect('basic')">
            <template #cover>
              <img alt="basic version" src="../assets/basic-version.jpg" />
            </template>
            <a-card-meta title="仅美食管理版" description="适合想探索美食的用户" />
          </a-card>
        </a-col>
      </a-row>
    </section>

    <!-- 第二个区块：卡路里管理功能 -->
    <section class="feature-section">
      <a-row align="middle">
        <a-col :span="12" class="feature-text">
          <h2>卡路里管理</h2>
          <p>科学计算每日摄入，合理规划饮食计划，帮助您实现健康饮食目标。</p>
          <ul>
            <li>每日卡路里追踪</li>
            <li>营养成分分析</li>
            <li>个性化饮食建议</li>
          </ul>
        </a-col>
        <a-col :span="12">
          <img src="../assets/calorie-management.jpg" alt="卡路里管理" />
        </a-col>
      </a-row>
    </section>

    <!-- 第三个区块：食材管理功能 -->
    <section class="feature-section alternate">
      <a-row align="middle">
        <a-col :span="12">
          <img src="../assets/ingredient-management.jpg" alt="食材管理" />
        </a-col>
        <a-col :span="12" class="feature-text">
          <h2>食材管理</h2>
          <p>智能管理您的食材库，让烹饪更加便捷高效。</p>
          <ul>
            <li>食材库存追踪</li>
            <li>保质期提醒</li>
            <li>智能采购清单</li>
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
            <li>基于现有食材的推荐</li>
            <li>营养均衡的搭配建议</li>
          </ul>
        </a-col>
        <a-col :span="12">
          <img src="../assets/recipe-recommendation.jpg" alt="菜谱推荐" />
        </a-col>
      </a-row>
    </section>

    <!-- 第五个区块：菜谱浏览与搜索功能 -->
    <section class="feature-section alternate">
      <a-row align="middle">
        <a-col :span="12">
          <img src="../assets/recipe-browse.jpg" alt="菜谱浏览" />
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
import { useRouter } from 'vue-router';

const router = useRouter();

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
}

.main-title {
  text-align: center;
  margin-bottom: 40px;
  color: #42b983;
}

.version-select {
  margin-bottom: 60px;
}

.feature-section {
  padding: 60px 20px;
  margin: 20px 0;
}

.feature-section.alternate {
  background-color: #f5f5f5;
}

.feature-text {
  padding: 0 40px;
}

.feature-text h2 {
  color: #42b983;
  margin-bottom: 20px;
}

.feature-text ul {
  list-style: none;
  padding: 0;
}

.feature-text ul li {
  margin: 10px 0;
  padding-left: 20px;
  position: relative;
}

.feature-text ul li:before {
  content: "•";
  color: #42b983;
  position: absolute;
  left: 0;
}

img {
  width: 100%;
  max-width: 500px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.ant-card {
  transition: transform 0.3s;
}

.ant-card:hover {
  transform: translateY(-5px);
  cursor: pointer;
}
</style>