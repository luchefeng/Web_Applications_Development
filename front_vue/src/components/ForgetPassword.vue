<template>
    <a-form
      :model="formState"
      v-bind="layout"
      name="nest-messages"
      :validate-messages="validateMessages"
      @finish="onFinish"
    >
      <a-form-item :name="['user', 'email']" label="Email" :rules="[{ type: 'email',required: true }]">
        <a-input v-model:value="formState.user.email" />
      </a-form-item>
      <a-form-item :name="['user', 'password']" label="password" :rules="[{ required: true }]">
        <a-input v-model:value="formState.user.password" />
      </a-form-item>
      <a-form-item :wrapper-col="{ ...layout.wrapperCol, offset: 8 }">
        <a-button type="primary" html-type="submit">Submit</a-button>
      </a-form-item>
    </a-form>
  </template>
  <script setup>
  import { reactive } from 'vue';
  const layout = {
    labelCol: {
      span: 8,
    },
    wrapperCol: {
      span: 16,
    },
  };
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
  const formState = reactive({
    user: {
      email: '',
      password: '',
    },
  });
  const onFinish = values => {
    console.log('Success:', values);
  };
  </script>