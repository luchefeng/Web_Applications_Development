<template>
  <div class="profile">
    <h1>User Profile</h1>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="user.username" id="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="user.email" id="email" required />
      </div>
      <div>
        <label for="calorieGoal">Calorie Goal:</label>
        <input type="number" v-model="user.calorie_goal" id="calorieGoal" required />
      </div>
      <button type="submit">Update Profile</button>
    </form>
    <div v-if="message">{{ message }}</div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      message: '',
    };
  },
  computed: {
    ...mapState(['user']),
  },
  methods: {
    async updateProfile() {
      try {
        const response = await this.$http.put('/api/profile', this.user);
        this.message = 'Profile updated successfully!';
      } catch (error) {
        this.message = 'Error updating profile.';
      }
    },
  },
  mounted() {
    // Fetch user data if needed
  },
};
</script>

<style scoped>
.profile {
  max-width: 400px;
  margin: auto;
}
</style>