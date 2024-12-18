<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <div>
        <label for="calorieGoal">Calorie Goal:</label>
        <input type="number" v-model="calorieGoal" required />
      </div>
      <button type="submit">Register</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      calorieGoal: 2000,
      errorMessage: ''
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post('/api/register', {
          username: this.username,
          email: this.email,
          password: this.password,
          calorie_goal: this.calorieGoal
        });
        if (response.data.success) {
          this.$router.push('/login');
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (error) {
        this.errorMessage = 'Registration failed. Please try again.';
      }
    }
  }
};
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: auto;
}
.error {
  color: red;
}
</style>