<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script setup>
import { computed, watch, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BasicLayout from './layouts/BasicLayout.vue';
import BasicLayout_calorie from './layouts/BasicLayout_calorie.vue';

const route = useRoute();
const router = useRouter();
const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true');

// 使用 ref 来追踪登录状态
const layout = computed(() => {
  return isLoggedIn.value ? BasicLayout_calorie : BasicLayout;
});

// 监听登录状态变化
watch(() => localStorage.getItem('isLoggedIn'), (newValue) => {
  isLoggedIn.value = newValue === 'true';
  if (!isLoggedIn.value) {
    router.push('/');
  }
}, { immediate: true });
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