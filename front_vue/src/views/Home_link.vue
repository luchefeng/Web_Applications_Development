<template>
    <div class = "home_link">
        <a-row>
            <a-col :flex="2"></a-col>
            <a-col :flex="1">
                <Login />
            </a-col>
            <a-col :flex="2"></a-col>
        </a-row>
    </div>
</template>

<script>
import Login from '@/components/Login.vue'; 

export default {
  name: 'Home_link',
  components: {
    Login
  },
};
</script>

<style scoped>
.home_link {
  text-align: center;
  margin-top: 50px;
}
</style>