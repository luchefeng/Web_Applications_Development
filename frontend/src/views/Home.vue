<template>
  <div class="home">
    <h1>Welcome to the Calorie Tracker</h1>
    <p>Log in to track your calorie intake and get personalized recipe recommendations!</p>
    <router-link to="/login">Login</router-link>
    <router-link to="/register">Register</router-link>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>
