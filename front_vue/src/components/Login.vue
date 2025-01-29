<template>
  <a-form
    :model="formState"
    name="normal_login"
    class="login-form"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
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
      Or
      <router-link to="/register">Register</router-link>
    </a-form-item>
  </a-form>
</template>

<script setup>
import { reactive, ref, computed } from 'vue';
import axios from 'axios';

const formState = reactive({
  username: '',
  password: '',
  remember: true,
});

const errorMessage = ref('');

const onFinish = async () => {
  try {
    const response = await axios.post('http://your-flask-backend-url/login', {
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

const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

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