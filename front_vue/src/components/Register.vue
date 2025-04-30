<template>
  <div class="register-container">
    <h1 class="register-title">注册</h1>
    <a-form :model="formState" name="normal_register" class="register-form" @finish="registerUser" @finishFailed="onFinishFailed">
      <a-form-item label="用户名" name="username" :rules="[{ required: true, message: '请输入您的用户名！' }]">
        <a-input v-model:value="formState.username">
          <template #prefix>
            <UserOutlined class="site-form-item-icon" />
          </template>
        </a-input>
      </a-form-item>

      <a-form-item label="邮箱" name="email" :rules="[{ required: true, message: '请输入您的邮箱！' }]">
        <a-input v-model:value="formState.email">
          <template #prefix>
            <MailOutlined class="site-form-item-icon" />
          </template>
        </a-input>
      </a-form-item>

      <a-form-item label="密码" name="password" :rules="[{ required: true, message: '请输入您的密码！' }]">
        <a-input-password v-model:value="formState.password">
          <template #prefix>
            <LockOutlined class="site-form-item-icon" />
          </template>
        </a-input-password>
      </a-form-item>

      <a-form-item name="calorieVersion">
        <a-row>
          <a-col :span="12">
            <a-checkbox v-model:checked="formState.calorieVersion">卡路里管理版本</a-checkbox>
          </a-col>
          <a-col :span="12">
            <a-checkbox v-model:checked="calorieVersionOpposite">菜谱推荐版本</a-checkbox>
          </a-col>
        </a-row>
      </a-form-item>

      <a-form-item>
        <a-button :disabled="disabled" type="primary" html-type="submit" class="register-form-button">
          注册
        </a-button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        已有账号？
        <router-link to="/login">登录</router-link>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watch, onUnmounted } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import { UserOutlined, MailOutlined, LockOutlined } from '@ant-design/icons-vue';

const router = useRouter();
const route = useRoute();

const formState = reactive({
  username: '',
  email: '',
  password: '',
  calorieVersion: true, // 默认选择卡路里管理版本
});

// 计算属性：反转 calorieVersion
const calorieVersionOpposite = computed({
  get: () => !formState.value.calorieVersion,
  set: (value) => {
    formState.value.calorieVersion = !value;
  },
});

const errorMessage = ref('');
const successMessage = ref('');

let isMounted = true;

const registerUser = async () => {
  try {
    const response = await axios.post('http://localhost:5000/users/register', {
      username: formState.username,
      email: formState.email,
      password: formState.password,
      calorieVersion: formState.calorieVersion, // 确保发送此字段
    });

    if (isMounted) {
      console.log('注册成功:', response.data);
      errorMessage.value = '';
      successMessage.value = '注册成功！请登录。';

      // 跳转到登录页面，并传递版本信息
      router.push({
        path: '/login',
        query: { version: formState.calorieVersion ? 'calorie' : 'cook' }
      });
    }
  } catch (error) {
    if (isMounted) {
      console.error('注册失败:', error);
      errorMessage.value = error.response?.data?.message || '注册失败，请重试。';
      successMessage.value = '';
    }
  }
};

onUnmounted(() => {
  isMounted = false;
});

const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

const disabled = computed(() => {
  return !(formState.username && formState.email && formState.password);
});
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

.register-form-button {
  width: 100%;
}

.error {
  color: red;
}

.success {
  color: green;
}
</style>