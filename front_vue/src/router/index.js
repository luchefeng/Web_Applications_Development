import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Start from '@/views/Start.vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import RegisterP from '@/views/RegisterP.vue'; // 导入新的 RegisterP 组件
import Profile from '@/views/Profile.vue';
import Recipes from '@/views/Recipes.vue';
import Articles from '@/views/Articles.vue';
import Home_link from '@/views/Home_link.vue';
import Dashboard from '@/views/Dashboard.vue'; // 导入 Dashboard 组件
import CalorieManagement from '@/views/Calorie_Management.vue'; // 新增，导入 CalorieManagement 组件

const routes = [
  { path: '/', component: Start },
  { path: '/home_link', component: Home_link },
  { path: '/start', component: Start },
  { path: '/login', component: Login },
  { path: '/register', component: Register }, // 更改为 RegisterP 组件
  { path: '/profile', component: Profile },
  { path: '/recipes', component: Recipes },
  { path: '/articles', component: Articles },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard // 使用导入的 Dashboard 组件
  },
  {
    path: '/calorie-management', // 新增的路由路径
    name: 'CalorieManagement',
    component: CalorieManagement // 使用导入的 CalorieManagement 组件
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
