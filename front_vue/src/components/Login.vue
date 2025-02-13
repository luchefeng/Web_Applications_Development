<template>
  <!-- 表單組件 -->
  <a-form
    :model="formState"
    name="normal_login"
    class="login-form"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
    <!-- 用戶名輸入框 -->
    <a-form-item
      label="Username"
      name="username"
      :rules="[{ required: true, message: '請輸入您的用戶名！' }]"
    >
      <a-input v-model:value="formState.username">
        <template #prefix>
          <UserOutlined class="site-form-item-icon" />
        </template>
      </a-input>
    </a-form-item>

    <!-- 密碼輸入框 -->
    <a-form-item
      label="Password"
      name="password"
      :rules="[{ required: true, message: '請輸入您的密碼！' }]"
    >
      <a-input-password v-model:value="formState.password">
        <template #prefix>
          <LockOutlined class="site-form-item-icon" />
        </template>
      </a-input-password>
    </a-form-item>

    <!-- 記住我複選框 -->
    <a-form-item>
      <a-form-item name="remember" no-style>
        <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>
      </a-form-item>
      <a class="login-form-forgot" href="">Forgot password</a>
    </a-form-item>

    <!-- 提交按鈕 -->
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
import { reactive, ref, computed } from 'vue'; // 導入 reactive、ref 和 computed 函數
import axios from 'axios'; // 導入 axios 庫，用於發送 HTTP 請求
import { useRouter } from 'vue-router';

const router = useRouter(); // 導入 Vue Router

// 表單狀態，使用 reactive 創建響應式對象
const formState = reactive({
  username: '',
  password: '',
  remember: true,
});

// 錯誤消息，使用 ref 創建響應式引用
const errorMessage = ref('');
// 成功消息，使用 ref 創建響應式引用
const successMessage = ref('');

// 表單提交處理函數
const onFinish = async () => {
  try {
    // 發送 POST 請求到後端登錄 API
    const response = await axios.post('http://localhost:5000/users/login', {
      username: formState.username,
      password: formState.password
    });
    console.log('Login successful:', response.data);
    errorMessage.value = ''; // 清除錯誤消息
    successMessage.value = '登錄成功！'; // 顯示登錄成功消息

    // 跳轉到儀表盤或其他頁面
    setTimeout(() => {
      router.push('/dashboard'); // 確保該路由存在
    }, 2000);
  } catch (error) {
    console.error('Login failed:', error);

    // 檢查錯誤響應並設置相應的錯誤消息
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
    successMessage.value = ''; // 清除成功消息
  }
};

// 表單提交失敗處理函數
const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

// 計算屬性，表單是否禁用
const disabled = computed(() => {
  return !(formState.username && formState.password);
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
