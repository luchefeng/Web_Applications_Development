<template>
  <div id="basic-layout">
    <a-space direction="vertical" :style="{ width: '100%' }" :size="[0, 48]">
      <a-layout>
        <a-layout-header class="header">
          <a-row>
            <a-col flex="3">
              <nav>
                <router-link to="/dashboard">Dashboard</router-link>
                <router-link to="/profile">Profile</router-link>
                <router-link to="/recipes">Recipes</router-link>
                <router-link to="/calorie-management">Calorie</router-link>
                <router-link to="/ingredient-management">Ingredient</router-link>
              </nav>                
            </a-col>
            <a-col flex="1"></a-col>
            <a-col flex="1">
              <nav class="right-nav">
                <a-avatar :size="32" icon="user" class="user-avatar" @click="goToProfile" />
                <a-button type="primary" @click="handleLogout">
                  Logout
                </a-button>
              </nav>
            </a-col>
          </a-row>            
        </a-layout-header>
        <a-layout-content class = "content">
          <router-view />
        </a-layout-content>
        <a-layout-footer class = "footer">
          <p>Calorie.ver</p>
        </a-layout-footer>
      </a-layout>
    </a-space>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';
import { UserOutlined } from '@ant-design/icons-vue';

const router = useRouter();

const handleLogout = async () => {
  try {
    console.log('Sending logout request...');
    const response = await axios.post('http://localhost:5000/users/logout', {}, {
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 5000 // 添加超时设置
    });

    if (response.status === 200) {
      // 清除本地存储
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('user');
      
      // 更新 store
      store.dispatch('logout');
      
      // 等待状态更新
      await Promise.resolve();
      
      // 跳转到首页
      await router.push('/');
      
      // 重新加载页面以确保状态完全重置
      window.location.reload();
    }
  } catch (error) {
    console.error('Logout error:', error);
    // 即使请求失败也清除本地状态
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('user');
    store.dispatch('logout');
    router.push('/');
  }
};

const goToProfile = () => {
  router.push('/profile');
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.header {
  background-color: #6ee2da;
  padding: 0px;
  position: fixed;        /* 固定定位 */
  top: 0;                /* 固定在顶部 */
  width: 100%;           /* 宽度100% */
  z-index: 1000;         /* 确保header在其他元素之上 */
}

nav {
  display: flex;
  justify-content: space-around;
  align-items: center; /* 垂直居中 */
  height: 100%; /* 确保导航栏占满高度 */
}

.right-nav {
  justify-content: flex-end;  /* 保持右对齐 */
  align-items: center;        /* 垂直居中 */
  height: 100%;              /* 占满高度 */
  gap: 16px;                 /* 增加按钮之间的间距 */
  padding-right: 24px;       /* 增加右侧内边距 */
}

.right-nav .ant-btn {
  display: flex;            /* 使按钮内容居中 */
  align-items: center;      /* 垂直居中 */
  justify-content: center;  /* 水平居中 */
}

.right-nav a {
  color: white; /* 链接文字颜色 */
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

nav a.router-link-exact-active {
  text-decoration: underline;
}

main {
  margin-top: 20px;
}

.footer {
  text-align: center;
  background-color: #6ee2da;
  color: white;
  padding: 10px;
  bottom: 0;
  width: 100%;
  /*
  position: static;
  margin-top: auto;
  */
}

.content {
  margin-top: 64px;      /* 为固定header留出空间，64px是header的高度 */
}

.user-avatar {
  cursor: pointer;  /* 添加手型光标 */
  transition: opacity 0.3s;  /* 添加过渡效果 */
}

.user-avatar:hover {
  opacity: 0.8;  /* 悬停时的透明度效果 */
}
</style>