import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Start from '@/views/Start.vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import Profile from '@/views/Profile.vue';
import Recipes from '@/views/Recipes.vue';
import RecipesRecommend from '@/views/Recipes_recommend.vue';
import RecipesSearch from '@/views/Recipes_view.vue';
import Articles from '@/views/Articles.vue';
import Home_link from '@/views/Home_link.vue';
import Dashboard from '@/views/Dashboard.vue';
import CalorieManagement from '@/views/Calorie_Management.vue';
import IngredientManagement from '@/views/Ingredient_Management.vue'; // 新增，導入 IngredientManagement 組件
import DashboardCalorie from '@/views/Dashboard_calorie.vue';
import DashboardCook from '@/views/Dashboard_cook.vue';

const routes = [
  { path: '/', component: Start },
  { path: '/home_link', component: Home_link },
  { path: '/start', component: Start },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/profile', component: Profile },
  { path: '/recipes', component: Recipes },
  { path: '/articles', component: Articles },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/calorie-management',
    name: 'CalorieManagement',
    component: CalorieManagement
  },
  {
    path: '/ingredient-management', // 新增的路由路徑
    name: 'IngredientManagement',
    component: IngredientManagement // 使用導入的 IngredientManagement 組件
  },
  {
    path: '/recipes-recommend',
    name: 'RecipesRecommend',
    component: RecipesRecommend
  },
  {
    path: '/recipes-search',
    name: 'RecipesSearch',
    component: RecipesSearch
  },
  {
    path: '/recipes/add',
    name: 'RecipesAdd',
    component: () => import('@/views/Recipes_add.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/recipes-view',
    name: 'Recipes',
    component: () => import('@/views/Recipes_view.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard-calorie',
    component: DashboardCalorie,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard-cook',
    component: DashboardCook,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
  
  // 需要登录的路由
  const requiresAuth = ['/dashboard', '/calorie-management', '/profile'];
  
  if (requiresAuth.includes(to.path) && !isLoggedIn) {
    next('/login');
  } else if (!isLoggedIn && from.path === '/dashboard') {
    // 确保状态更新后再跳转
    await Promise.resolve();
    next('/');
  } else {
    next();
  }
});

export default router;
