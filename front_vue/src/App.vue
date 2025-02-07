<template>
  <div id="app">
    <basic-layout />
  </div>
</template>

<script>
import BasicLayout from '@/layouts/BasicLayout.vue';

export default {
  name: 'App',
  components: {
    BasicLayout,
  },
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
</style>