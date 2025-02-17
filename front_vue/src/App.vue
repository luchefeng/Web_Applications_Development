<template>
  <div id="app">
    <header>
      <nav>
        <router-link to="/home">Home</router-link>
        <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
        <router-link v-if="!isLoggedIn" to="/register">Register</router-link>
        <button v-if="isLoggedIn" @click="logout">Logout</button>
      </nav>
    </header>
    <component :is="layout">
      <router-view />
    </component>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BasicLayout from './layouts/BasicLayout.vue';
import BasicLayout_calorie from './layouts/BasicLayout_calorie.vue';
import axios from 'axios';
import { useStore } from 'vuex';

const route = useRoute();
const router = useRouter();
const store = useStore();

const isLoggedIn = computed(() => store.state.isLoggedIn);

// 使用 computed 來追踪登錄狀態
const layout = computed(() => {
  return isLoggedIn.value ? BasicLayout_calorie : BasicLayout;
});

const logout = async () => {
  try {
    console.log('Sending logout request...'); // 添加調試信息
    const response = await axios.post('http://localhost:5000/users/logout', {}, { withCredentials: true });
    console.log('Logout request sent:', response.data); // 添加調試信息

    // 確保正確地更新 Vuex 狀態和本地存儲
    store.commit('setLoggedIn', false);
    localStorage.setItem('isLoggedIn', 'false');

    // 跳轉到最開始的頁面
    router.push('/');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

// 監聽登錄狀態變化
watch(isLoggedIn, (newValue) => {
  console.log('Logged in status changed:', newValue); // 添加調試信息
  if (!newValue) {
    router.push('/');
  }
});

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>