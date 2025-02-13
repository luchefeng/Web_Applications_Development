<template>
  <div class="dashboard">
    <h1>歡迎，{{ user.username }}</h1>
    <p>這是您的儀表盤頁面。</p>

    <div class="user-info">
      <h2>個人信息</h2>
      <p><strong>用戶名：</strong> {{ user.username }}</p>
      <p><strong>電子郵件：</strong> {{ user.email }}</p>
    </div>

    <div class="actions">
      <router-link to="/edit-profile">編輯個人信息</router-link>
      <router-link to="/logout">登出</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user = ref({
  username: '',
  email: ''
});

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:5000/user-info');
    user.value = response.data;
  } catch (error) {
    console.error('Failed to fetch user info:', error);
  }
});
</script>

<style scoped>
.dashboard {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.user-info {
  margin-top: 20px;
}

.actions {
  margin-top: 20px;
}

.actions a {
  margin-right: 10px;
}
</style>
