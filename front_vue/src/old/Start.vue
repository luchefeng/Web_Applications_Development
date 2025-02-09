<template>
  <div>
    <a-form @submit="handleSubmit">
      <a-form-item>
        <a-input v-model="form.username" placeholder="Username" />
      </a-form-item>
      <a-form-item>
        <a-input v-model="form.password" type="password" placeholder="Password" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">Submit</a-button>
      </a-form-item>
    </a-form>
    <a-row>
      <a-col v-for="feature in features" :key="feature.title" :span="8">
        <a-card :title="feature.title">
          <p>{{ feature.description }}</p>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { ref } from 'vue';
import { Form, Input, Button, Card, List, Row, Col } from 'ant-design-vue';

export default {
  name: 'Start',
  setup() {
    const form = ref({
      username: '',
      password: ''
    });

    const handleSubmit = () => {
      console.log('Form submitted:', form.value);
    };

    const features = [
      { title: '食材管理', description: '管理和查看各种食材的信息。' },
      { title: '卡路里管理', description: '记录和管理每日摄入的卡路里。' },
      { title: '菜谱推荐', description: '根据食材和卡路里推荐健康菜谱。' }
    ];

    return {
      form,
      handleSubmit,
      features
    };
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>