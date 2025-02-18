<template>
  <div class="profile-container">
    <h2>个人资料</h2>
    <a-form :model="profileForm" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
      <!-- 头像上传 -->
      <a-form-item label="头像">
        <a-upload
          v-model:file-list="fileList"
          list-type="picture-circle"
          :show-upload-list="false"
          @change="handleAvatarChange"
        >
          <div v-if="!profileForm.avatar_url">
            <plus-outlined />
            <div style="margin-top: 8px">上传</div>
          </div>
          <img
            v-else
            :src="profileForm.avatar_url"
            alt="avatar"
            style="width: 100%"
          />
        </a-upload>
      </a-form-item>

      <!-- 基本信息 -->
      <a-form-item label="昵称">
        <a-input v-model:value="profileForm.nickname" />
      </a-form-item>

      <a-form-item label="性别">
        <a-radio-group v-model:value="profileForm.gender">
          <a-radio value="male">男</a-radio>
          <a-radio value="female">女</a-radio>
          <a-radio value="other">其他</a-radio>
        </a-radio-group>
      </a-form-item>

      <a-form-item label="邮箱">
        <a-input v-model:value="profileForm.email" />
      </a-form-item>

      <a-form-item label="账户版本">
        <a-tag :color="profileForm.calorie_version ? 'green' : 'blue'">
          {{ profileForm.calorie_version ? '卡路里管理版' : '基础版' }}
        </a-tag>
      </a-form-item>

      <!-- 卡路里目标（仅卡路里版显示） -->
      <template v-if="profileForm.calorie_version">
        <a-form-item label="卡路里目标">
          <a-input-number 
            v-model:value="profileForm.calorie_goal" 
            :min="1000" 
            :max="5000"
          /> kcal/天
        </a-form-item>
      </template>

      <!-- 密码修改 -->
      <a-form-item label="修改密码">
        <a-button type="link" @click="showPasswordModal = true">
          修改密码
        </a-button>
      </a-form-item>

      <!-- 保存按钮 -->
      <a-form-item :wrapper-col="{ offset: 6, span: 14 }">
        <a-button type="primary" @click="handleSubmit">保存更改</a-button>
      </a-form-item>
    </a-form>

    <!-- 密码修改弹窗 -->
    <a-modal
      v-model:visible="showPasswordModal"
      title="修改密码"
      @ok="handlePasswordChange"
      @cancel="handlePasswordCancel"
    >
      <a-form :model="passwordForm">
        <a-form-item label="当前密码" required>
          <a-input-password v-model:value="passwordForm.oldPassword" />
        </a-form-item>
        <a-form-item label="新密码" required>
          <a-input-password v-model:value="passwordForm.newPassword" />
        </a-form-item>
        <a-form-item label="确认新密码" required>
          <a-input-password v-model:value="passwordForm.confirmPassword" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import axios from 'axios';

const profileForm = ref({
  nickname: '',
  gender: 'other',
  email: '',
  avatar_url: '',
  calorie_version: false,
  calorie_goal: 2000
});

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const showPasswordModal = ref(false);
const fileList = ref([]);

// 获取用户信息
const fetchUserProfile = async () => {
  try {
    const response = await axios.get('http://localhost:5000/users/profile', {
      withCredentials: true
    });
    profileForm.value = { ...response.data };
  } catch (error) {
    message.error('获取用户信息失败');
  }
};

// 保存个人资料
const handleSubmit = async () => {
  try {
    await axios.put('http://localhost:5000/users/profile', profileForm.value, {
      withCredentials: true
    });
    message.success('保存成功');
  } catch (error) {
    message.error('保存失败');
  }
};

// 处理头像上传
const handleAvatarChange = (info) => {
  if (info.file.status === 'done') {
    profileForm.value.avatar_url = info.file.response.url;
    message.success('头像上传成功');
  }
};

// 处理密码修改
const handlePasswordChange = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    message.error('两次输入的密码不一致');
    return;
  }

  try {
    await axios.put('http://localhost:5000/users/change-password', {
      oldPassword: passwordForm.value.oldPassword,
      newPassword: passwordForm.value.newPassword
    }, { withCredentials: true });
    
    message.success('密码修改成功');
    showPasswordModal.value = false;
    passwordForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' };
  } catch (error) {
    message.error('密码修改失败');
  }
};

const handlePasswordCancel = () => {
  showPasswordModal.value = false;
  passwordForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' };
};

onMounted(() => {
  fetchUserProfile();
});
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>