<template>
  <div class="home">
    <h1>Welcome to the Calorie Tracker</h1>
    <a-divider>With Text</a-divider>
    <a-row>
      <a-col :flex="3">
        <p>Log in to track your calorie intake and get personalized recipe recommendations!</p>
      </a-col>
      <a-col :flex="1">
        <a-col>
          <a-row :flex="2">        
            <div><Login /></div>
          </a-row>
          <a-row :flex="2">
            <router-link to="/register">Register</router-link>
          </a-row>
        </a-col>
      </a-col>
    </a-row>

  </div>
</template>

<script>
import Login from '@/components/Login.vue'; // 确保路径正确

export default {
  name: 'Home',
  components: {
    Login
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>