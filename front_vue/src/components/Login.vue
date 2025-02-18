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
    // 先验证验证码
    const captchaResponse = await axios.post('http://localhost:5000/users/verify-captcha', {
      captcha: formState.captcha,
    }, { withCredentials: true });

    if (captchaResponse.data.message !== '驗證碼正確！') {
      throw new Error('Captcha validation failed');
    }

    // 验证码正确后，调用登录
    const response = await axios.post('http://localhost:5000/users/login', {
      username: formState.username,
      password: formState.password,
      captcha: formState.captcha,
    }, { withCredentials: true });

    console.log('登录成功:', response.data);
    errorMessage.value = '';  // 清除错误消息
    successMessage.value = '登录成功！';  // 显示成功消息

    // 存储登录状态
    localStorage.setItem('isLoggedIn', 'true');

    // 更新 Vuex 中的登录状态
    store.commit('setLoggedIn', true);

    // 根据用户选择的版本跳转到不同的仪表盘
    const userInfoResponse = await axios.get('http://localhost:5000/users/user-info', { withCredentials: true });
    const user = userInfoResponse.data;

    if (user.calorieVersion) {
      router.push({ path: '/dashboard-calorie' });
    } else {
      router.push({ path: '/dashboard-cook' });
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