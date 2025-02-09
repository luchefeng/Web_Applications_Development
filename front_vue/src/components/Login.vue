<template>
  <!-- 表单组件 -->
  <a-form
    :model="formState"
    name="normal_login"
    class="login-form"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
    <!-- 用户名输入框 -->
    <a-form-item
      label="Username"
      name="username"
      :rules="[{ required: true, message: 'Please input your username!' }]"
    >
      <a-input v-model:value="formState.username">
        <template #prefix>
          <UserOutlined class="site-form-item-icon" />
        </template>
      </a-input>
    </a-form-item>

    <!-- 密码输入框 -->
    <a-form-item
      label="Password"
      name="password"
      :rules="[{ required: true, message: 'Please input your password!' }]"
    >
      <a-input-password v-model:value="formState.password">
        <template #prefix>
          <LockOutlined class="site-form-item-icon" />
        </template>
      </a-input-password>
    </a-form-item>

    <!-- 记住我复选框 -->
    <a-form-item>
      <a-form-item name="remember" no-style>
        <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>
      </a-form-item>
      <a class="login-form-forgot" href="">Forgot password</a>
    </a-form-item>

    <!-- 提交按钮 -->
    <a-form-item>
      <a-button :disabled="disabled" type="primary" html-type="submit" class="login-form-button">
        Log in
      </a-button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      Or
      <router-link to="/register">Register</router-link>
    </a-form-item>
  </a-form>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'; // 导入 reactive、ref 和 computed 函数
import axios from 'axios'; // 导入 axios 库，用于发送 HTTP 请求

// 表单状态，使用 reactive 创建响应式对象
const formState = reactive({
  username: '',
  password: '',
  remember: true,
});

// 错误消息，使用 ref 创建响应式引用
const errorMessage = ref('');

// 表单提交处理函数
const onFinish = async () => {
  try {
    // 发送 POST 请求到后端登录 API
    const response = await axios.post('http://localhost:5000/login', {
      username: formState.username,
      password: formState.password
    });
    console.log('Login successful:', response.data);
    errorMessage.value = ''; // 清除错误消息
  } catch (error) {
    console.error('Login failed:', error);
    errorMessage.value = 'Invalid username or password';
  }
};

// 表单提交失败处理函数
const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

// 计算属性，表单是否禁用
const disabled = computed(() => {
  return !(formState.username && formState.password);
});
</script>

<style scoped>
#components-form-demo-normal-login .login-form {
  max-width: 300px;
}
#components-form-demo-normal-login .login-form-forgot {
  float: right;
}
#components-form-demo-normal-login .login-form-button {
  width: 100%;
}
.error {
  color: red;
}
</style>