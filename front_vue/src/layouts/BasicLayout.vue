<template>
    <div id="basic-layout">
      <a-space direction="vertical" :style="{ width: '100%' }" :size="[0, 48]">
        <a-layout>
          <a-layout-header class="header">
            <nav>
              <router-link to="/">Home</router-link>
              <router-link to="/login">Login</router-link>
              <router-link to="/register">Register</router-link>
              <router-link to="/profile">Profile</router-link>
              <router-link to="/recipes">Recipes</router-link>
              <router-link to="/articles">Articles</router-link>
            </nav>            
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

<script lang="ts" setup>
</script>

<style scoped>
  
  .header {
    background-color: #42b983;
    padding: 10px;
  }
  
  nav {
    display: flex;
    justify-content: space-around;
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
    position: fixed;
    bottom: 0;
    width: 100%;
  }
</style>