import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import Profile from '@/views/Profile.vue';
import Recipes from '@/views/Recipes.vue';
import Articles from '@/views/Articles.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/profile', component: Profile },
  { path: '/recipes', component: Recipes },
  { path: '/articles', component: Articles },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;