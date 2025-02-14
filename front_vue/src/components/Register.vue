<template>
  <div class="register-container">
    <h1 class="register-title">Register</h1>
    <!-- 表单组件 -->
    <a-form
      :model="formState"
      v-bind="layout"
      name="nest-messages"
      :validate-messages="validateMessages"
      @finish="onFinish"
      class="register-form"
    >
      <!-- 用户名输入框 -->
      <a-form-item :name="['user', 'name']" label="Name" :rules="[{ required: true }]">
        <a-input v-model:value="formState.user.name" />
      </a-form-item>
      <!-- 电子邮件输入框 -->
      <a-form-item :name="['user', 'email']" label="Email" :rules="[{ type: 'email',required: true }]">
        <a-input v-model:value="formState.user.email" />
      </a-form-item>
      <!-- 密码输入框 -->
      <a-form-item :name="['user', 'password']" label="password" :rules="[{ required: true }]">
        <a-input-password v-model:value="formState.user.password" />
      </a-form-item>
      <!-- 卡路里目标输入框 -->
      <a-form-item :name="['user', 'calorie goal']" label="calorie goal" :rules="[{ type: 'number', min: 0, max: 10000 }]">
        <a-input-number v-model:value="formState.user.calorie_goal" />
      </a-form-item>
      <!-- 介绍输入框 -->
      <a-form-item :name="['user', 'introduction']" label="Introduction">
        <a-textarea v-model:value="formState.user.introduction" />
      </a-form-item>
      <!-- 提交按钮 -->
      <a-form-item :wrapper-col="{ ...layout.wrapperCol, offset: 8 }">
        <a-button type="primary" html-type="submit">Submit</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'; // 导入 reactive 函数，用于创建响应式状态
import axios from 'axios'; // 导入 axios 库，用于发送 HTTP 请求
import { useRouter } from 'vue-router'; // 导入 useRouter 函数，用于页面跳转

// 表单布局配置
const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};

// 表单验证消息配置
const validateMessages = {
  required: '${label} is required!',
  types: {
    email: '${label} is not a valid email!',
    number: '${label} is not a valid number!',
  },
  number: {
    range: '${label} must be between ${min} and ${max}',
  },
};

// 表单状态，使用 reactive 创建响应式对象
const formState = reactive({
  user: {
    name: '',
    calorie_goal: '',
    email: '',
    password: '',
    introduction: '',
  },
});

// 使用 Vue Router 进行页面跳转
const router = useRouter();

// 表单提交处理函数
const onFinish = async () => {
  try {
    // 发送 POST 请求到后端注册 API
    const response = await axios.post('http://localhost:5000/users/register', {
      username: formState.user.name,
      email: formState.user.email,
      password: formState.user.password,
      calorie_goal: formState.user.calorie_goal,
      introduction: formState.user.introduction,
    });
    console.log('Registration successful:', response.data);
    // 注册成功后跳转到登录页面
    router.push('/login');
  } catch (error) {
    console.error('Registration failed:', error);
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.register-title {
  margin-bottom: 24px;
  font-size: 24px;
  font-weight: bold;
}

.register-form {
  width: 400px;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>