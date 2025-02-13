<template>
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
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

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
    // 先驗證驗證碼
    const captchaResponse = await axios.post('http://localhost:5000/users/verify-captcha', {
      captcha: formState.captcha,
    }, {
      withCredentials: true
    });

    if (captchaResponse.data.message !== '驗證碼正確！') {
      throw new Error('Captcha validation failed');
    }

    // 驗證碼正確後，調用登錄
    const response = await axios.post('http://localhost:5000/users/login', {
      username: formState.username,
      password: formState.password,
      captcha: formState.captcha,
    }, {
      withCredentials: true
    });

    console.log('Login successful:', response.data);
    errorMessage.value = '';
    successMessage.value = '登錄成功！';

    setTimeout(() => {
      router.push('/dashboard');
    }, 2000);
  } catch (error) {
    console.error('Login failed:', error);

    if (error.response) {
      switch (error.response.status) {
        case 400:
          errorMessage.value = '錯誤請求：請檢查您的輸入。';
          break;
        case 401:
          errorMessage.value = '未授權：無效的用戶名或密碼。';
          break;
        case 404:
          errorMessage.value = '未找到：請求的資源未找到。';
          break;
        case 500:
          errorMessage.value = '內部服務器錯誤：請稍後再試。';
          break;
        default:
          errorMessage.value = `錯誤：${error.response.statusText}`;
      }
    } else {
      errorMessage.value = '網絡錯誤：請檢查您的網絡連接。';
    }
    successMessage.value = '';
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
.login-form {
  max-width: 300px;
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