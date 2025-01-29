<template>
    <div class="login">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div>
          <label for="username">Username:</label>
          <input type="text" v-model="username" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import axios from 'axios';
  
  export default {
    name: 'Login',
    setup() {
      const username = ref('');
      const password = ref('');
      const errorMessage = ref('');
  
      const login = async () => {
        try {
          const response = await axios.post('/api/login', {
            username: username.value,
            password: password.value,
          });
          // Handle successful login (e.g., redirect or store token)
        } catch (error) {
          errorMessage.value = 'Invalid username or password';
        }
      };
  
      return {
        username,
        password,
        errorMessage,
        login,
      };
    },
  };
  </script>
  
  <style scoped>
  .login {
    max-width: 400px;
    margin: auto;
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .error {
    color: red;
  }
  </style>