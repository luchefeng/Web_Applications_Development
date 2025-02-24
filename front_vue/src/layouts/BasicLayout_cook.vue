<template>
  <div id="basic-layout">
    <a-space direction="vertical" :style="{ width: '100%' }" :size="[0, 48]">
      <a-layout>
        <a-layout-header class="header">
          <a-row>
            <a-col flex="3">
              <nav>
                <a-col flex="1">
                  <a-button type="primary" class="nav-button">
                    <router-link to="/dashboard-cook">导航</router-link>
                  </a-button>
                </a-col>
                <a-col flex="1">
                  <a-button type="primary" class="nav-button">
                    <router-link to="/ingredient-management">食材管理</router-link>
                  </a-button>
                </a-col>
                <a-col flex="1">
                  <a-button type="primary" class="nav-button">
                    <router-link to="/recipes-view">菜谱浏览</router-link>
                  </a-button>
                </a-col>
                <a-col flex="1">
                  <a-button type="primary" class="nav-button">
                    <router-link to="/recipes/add">上传菜谱</router-link>
                  </a-button>
                </a-col>
              </nav>                 
            </a-col>
            <a-col flex="1"></a-col>
            <a-col flex="1">
              <nav class="right-nav">
                <a-avatar :size="32" icon="我" class="user-avatar" @click="goToProfile" />
                <a-button type="primary" @click="handleLogout"  class="custom-button">
                  登出
                </a-button>
              </nav>
            </a-col>
          </a-row>            
        </a-layout-header>
        <a-layout-content class = "content">
          <router-view />
        </a-layout-content>
        <a-layout-footer class = "footer">
          <p>Cook.ver</p>
        </a-layout-footer>
      </a-layout>
    </a-space>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';  // 添加这行
import axios from 'axios';

const router = useRouter();
const store = useStore();  // 添加这行

const handleLogout = async () => {
  try {
    const response = await axios.post('http://localhost:5000/users/logout', {}, {
      withCredentials: true
    });

    if (response.status === 200) {
      // 使用 store action 清理状态
      await store.dispatch('logout');
      
      // 跳转到首页
      await router.push('/');
      
      window.location.reload();
    }
  } catch (error) {
    console.error('Logout error:', error);
    // 即使请求失败也清除状态
    await store.dispatch('logout');
    await router.push('/');
    window.location.reload();
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
  background-color: #42b983;
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
  background-color: #42b983;
  color: white;
  padding: 10px;
  margin-top: auto;   /* 修改这行 */
  bottom: 0;
  width: 100%;
  /*
  position: static;
  margin-top: auto;
  */
}

.content {
  margin-top: 64px;      /* 为固定header留出空间，64px是header的高度 */
  flex: 1;           /* 添加这行，让内容区域自动填充空间 */
  padding: 24px;     /* 添加内边距 */
}

.user-avatar {
  cursor: pointer;  /* 添加手型光标 */
  transition: opacity 0.3s;  /* 添加过渡效果 */
}

.user-avatar:hover {
  opacity: 0.8;  /* 悬停时的透明度效果 */
}
.nav-button {
    background-color: #42b983 !important;
    border-color: #42b983 !important;
    color: white !important;
  }

  .nav-button:hover {
    background-color: #97f6d8 !important;
    border-color: #97f6d8  !important;
  }
  
  .custom-button {
    background-color: #42b983 !important;
    border-color: #fcfdfc !important;
    color: white !important;
  }

  .custom-button:hover {
    background-color: #97f6d8 !important;
    border-color: #fbfbfb !important;
    opacity: 0.9;
  }

  .custom-button a {
    color: white !important;
  }

#basic-layout {
  min-height: 100vh;  /* 添加这行，确保最小高度为视窗高度 */
  display: flex;      /* 添加这行 */
  flex-direction: column; /* 添加这行 */
}

.ant-layout {
  min-height: 100vh;  /* 添加这行 */
  display: flex;      /* 添加这行 */
  flex-direction: column; /* 添加这行 */
}
</style>