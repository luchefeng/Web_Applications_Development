<template>
    <div id="basic-layout">
      <a-space direction="vertical" :style="{ width: '100%' }" :size="[0, 48]">
        <a-layout>
          <a-layout-header class="header">
            <a-row>
              <a-col flex="3">
                <nav>
                  <router-link to="/">Home</router-link>
                  <router-link to="/profile">Profile</router-link>
                  <router-link to="/recipes">Recipes</router-link>
                  <router-link to="/articles">Articles</router-link>
                </nav>                
              </a-col>
              <a-col flex="1"></a-col>
              <a-col flex="1">
                <nav class="right-nav">
                  <template v-if="isLoggedIn">
                    <a-avatar :size="32" icon="user" />
                    <a-button type="primary" @click="handleLogout">
                      Logout
                    </a-button>
                  </template>
                  <template v-else>
                    <a-button type="primary">
                      <router-link to="/register">Register</router-link>
                    </a-button>
                    <a-button type="primary">
                      <router-link to="/login">Login</router-link>
                    </a-button>
                  </template>
                </nav>
              </a-col>
            </a-row>            
          </a-layout-header>
          <a-layout-content class = "content">
            <router-view />
          </a-layout-content>
          <a-layout-footer class = "footer">
            <p>Calorie Tracker V0.0</p>
          </a-layout-footer>
        </a-layout>
      </a-space>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoggedIn = ref(false);

onMounted(() => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';
});

const handleLogout = async () => {
  try {
    await axios.post('http://localhost:5000/users/logout', {}, { withCredentials: true });
    localStorage.removeItem('isLoggedIn');
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
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

</style>