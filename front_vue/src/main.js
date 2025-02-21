import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import intersect from './directives/intersect';

const app = createApp(App);
app.use(Antd)
  .use(router)
  .use(store);
app.directive('intersect', intersect);
app.mount('#app');