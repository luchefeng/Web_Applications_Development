<template>
  <div class="profile-container">
    <h2>个人资料</h2>
    <a-form :model="profileForm" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
      <!-- 基本信息 -->
      <a-form-item label="用户名">
        <a-input v-model:value="profileForm.username" disabled />
      </a-form-item>

      <a-form-item label="昵称">
        <a-input v-model:value="profileForm.profile.nickname" />
      </a-form-item>

      <a-form-item label="邮箱">
        <a-input v-model:value="profileForm.email" disabled />
      </a-form-item>

      <a-form-item label="个性签名">
        <a-textarea v-model:value="profileForm.profile.bio" :rows="4" />
      </a-form-item>

      <a-form-item label="账户版本">
        <a-tag :color="profileForm.calorie_version ? 'green' : 'blue'">
          {{ profileForm.calorie_version ? '卡路里管理版' : '仅美食管理版' }}
        </a-tag>
      </a-form-item>

      <!-- 卡路里目标（仅卡路里版显示） -->
      <template v-if="profileForm.calorie_version">
        <a-form-item label="每日卡路里目标">
          <a-input-number
            v-model:value="profileForm.calorie_goal"
            :min="1000"
            :max="5000"
          /> kcal/天
        </a-form-item>
      </template>

      <!-- 保存按钮 -->
      <a-form-item :wrapper-col="{ offset: 6, span: 14 }">
        <a-button type="primary" @click="handleSubmit">保存更改</a-button>
      </a-form-item>
    </a-form>

    <!-- 密码修改按钮和弹窗 -->
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
import { ref, onMounted, onActivated } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';  // 使用默认的 Axios 引入

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true  // 默认携带凭证
});

const profileForm = ref({
  username: '',
  email: '',
  calorie_version: false,
  calorie_goal: 2000,
  profile: {
    nickname: '',
    bio: '',
    avatar_url: ''
  }
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
    const response = await axiosInstance.get('/users/user-info');

    // 合并用户信息
    profileForm.value = {
      ...response.data,
      profile: response.data.profile || {
        nickname: '',
        bio: '',
        avatar_url: ''
      }
    };
  } catch (error) {
    message.error('获取用户信息失败');
    console.error('Error fetching profile:', error);
  }
};

// 保存个人资料
const handleSubmit = async () => {
  try {
    const updateData = {
      profile: {
        nickname: profileForm.value.profile.nickname,
        bio: profileForm.value.profile.bio
      }
    };

    if (profileForm.value.calorie_version) {
      updateData.calorie_goal = profileForm.value.calorie_goal;
    }

    await axiosInstance.put('/users/profile', updateData);
    message.success('保存成功');

    // 更新卡路里目标到界面
    if (profileForm.value.calorie_version) {
      profileForm.value.calorie_goal = updateData.calorie_goal;
    }
  } catch (error) {
    message.error('保存失败');
    console.error('Error updating profile:', error);
  }
};

// 处理头像上传
const handleAvatarChange = (info) => {
  if (info.file.status === 'done') {
    profileForm.value.profile.avatar_url = info.file.response.url;
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
    await axiosInstance.put('/users/change-password', {
      oldPassword: passwordForm.value.oldPassword,
      newPassword: passwordForm.value.newPassword
    });

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

// Add onActivated hook to refresh data when component is shown (for keep-alive)
onActivated(() => {
  fetchUserProfile();
});

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