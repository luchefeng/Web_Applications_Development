<template>
  <div class="login-container">
    <h1 class="login-title">Login</h1>
    <a-form :model="formState" name="normal_login" class="login-form" @finish="onFinish" @finishFailed="onFinishFailed">
      <a-form-item label="Username" name="username" :rules="[{ required: true, message: '請輸入您的用戶名！' }]">
        <a-input v-model:value="formState.username">
          <template #prefix>
            <UserOutlined class="site-form-item-icon" />
          </template>
        </a-input>
      </a-form-item>

      <a-form-item label="Password" name="password" :rules="[{ required: true, message: '請輸入您的密碼！' }]">
        <a-input-password v-model:value="formState.password">
          <template #prefix>
            <LockOutlined class="site-form-item-icon" />
          </template>
        </a-input-password>
      </a-form-item>

      <a-form-item label="Captcha">
        <div style="display: flex; align-items: center;">
          <img :src="captchaUrl" @click="fetchCaptcha" style="cursor: pointer; margin-right: 10px;">
          <a-input v-model:value="formState.captcha" placeholder="Enter captcha">
            <template #prefix>
              <SafetyOutlined class="site-form-item-icon" />
            </template>
          </a-input>
        </div>
      </a-form-item>

      <a-form-item>
        <a-form-item name="remember" no-style>
          <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>
        </a-form-item>
        <a class="login-form-forgot" href="">Forgot password</a>
      </a-form-item>

      <a-form-item>
        <a-button :disabled="disabled" type="primary" html-type="submit" class="login-form-button">
          Log in
        </a-button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        Or
        <router-link to="/register">Register</router-link>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore();

const formState = reactive({
  username: '',
  password: '',
  captcha: '',
  remember: true,
});

const errorMessage = ref('');
const successMessage = ref('');
const captchaUrl = ref('');

const fetchCaptcha = async () => {
  captchaUrl.value = `http://localhost:5000/users/generate-captcha?_t=${new Date().getTime()}`;
};

onMounted(fetchCaptcha);

const onFinish = async () => {
  try {
    const response = await axios.post('http://localhost:5000/users/login', formState, {
      withCredentials: true
    });

    if (response.status === 200) {
      const { calorie_version, user_id } = response.data;
      console.log('User version:', calorie_version);
      console.log('User ID from backend:', user_id);

      if (user_id) {
        localStorage.setItem('user_id', user_id);
        console.log('Stored user_id in localStorage:', user_id);
      } else {
        console.error('Backend did not return a valid user_id');
      }

      // 根据后端返回的版本信息设置布局
      const layoutType = calorie_version ? 'BasicLayout_calorie' : 'BasicLayout_cook';
      store.commit('setLayout', layoutType);
      store.commit('setLoginStatus', true);

      // 存储用户信息
      store.commit('setUser', {
        username: response.data.username,
        email: response.data.email,
        calorie_version: calorie_version
      });

      // 根据版本跳转到相应的仪表板
      router.push(calorie_version ? '/dashboard-calorie' : '/dashboard-cook');
    }
  } catch (error) {
    console.error('登录失败:', error);
    // 错误提示信息
    errorMessage.value = error.response?.data?.message || '登录失败，请重试。';
    successMessage.value = '';  // 清除成功消息
  }
};

const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

const disabled = computed(() => {
  return !(formState.username && formState.password && formState.captcha);
});
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.login-title {
  margin-bottom: 24px;
  font-size: 24px;
  font-weight: bold;
}

.login-form {
  width: 400px;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.login-form-forgot {
  float: right;
}

.login-form-button {
  width: 100%;
}

.error {
  color: red;
}

.success {
  color: green;
}
</style>