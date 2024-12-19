<template>
    <div id="app">
      <header>
        <nav>
          <router-link to="/">Home</router-link>
          <router-link to="/login">Login</router-link>
          <router-link to="/register">Register</router-link>
          <router-link to="/profile">Profile</router-link>
          <router-link to="/recipes">Recipes</router-link>
          <router-link to="/articles">Articles</router-link>
        </nav>
      </header>
      <main>
        <router-view />
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'App',
  };
  </script>
  
  <style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  
  header {
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
  </style>