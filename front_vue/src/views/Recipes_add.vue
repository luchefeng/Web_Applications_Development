<template>
  <div class="recipe-form">
    <h2>创建新菜谱</h2>
    <a-form
      :model="formState"
      :label-col="{ span: 4 }"
      :wrapper-col="{ span: 16 }"
      @finish="onFinish"
    >
      <!-- 菜谱名称 -->
      <a-form-item label="菜谱名称" name="title" :rules="[{ required: true, message: '请输入菜谱名称' }]">
        <a-input v-model:value="formState.title" placeholder="请输入菜谱名称" />
      </a-form-item>

      <!-- 食材列表 -->
      <a-form-item label="食材清单" name="ingredients">
        <a-space direction="vertical" style="width: 100%">
          <div v-for="(ingredient, index) in formState.ingredientList" :key="index" style="display: flex; gap: 8px;">
            <a-input v-model:value="ingredient.name" placeholder="食材名称" style="width: 40%" />
            <a-input-number v-model:value="ingredient.amount" placeholder="数量" style="width: 30%" />
            <a-select v-model:value="ingredient.unit" style="width: 20%">
              <a-select-option value="克">克</a-select-option>
              <a-select-option value="个">个</a-select-option>
              <a-select-option value="份">份</a-select-option>
            </a-select>
            <a-button type="link" danger @click="removeIngredient(index)">删除</a-button>
          </div>
          <a-button type="dashed" block @click="addIngredient">+ 添加食材</a-button>
        </a-space>
      </a-form-item>

      <!-- 烹饪步骤 -->
      <a-form-item label="烹饪步骤" name="instructions">
        <a-space direction="vertical" style="width: 100%">
          <div v-for="(step, index) in formState.cookingSteps" :key="index" style="display: flex; gap: 8px;">
            <span style="width: 30px">{{ index + 1 }}.</span>
            <a-textarea v-model:value="step.content" placeholder="请输入烹饪步骤" :rows="2" style="flex-grow: 1" />
            <a-button type="link" danger @click="removeStep(index)">删除</a-button>
          </div>
          <a-button type="dashed" block @click="addStep">+ 添加步骤</a-button>
        </a-space>
      </a-form-item>

      <!-- 提交按钮 -->
      <a-form-item :wrapper-col="{ offset: 4, span: 16 }">
        <a-button type="primary" html-type="submit">保存菜谱</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const formState = reactive({
  title: '',
  ingredientList: [{ name: '', amount: 1, unit: '克' }],
  cookingSteps: [{ content: '' }]
});

const addIngredient = () => {
  formState.ingredientList.push({ name: '', amount: 1, unit: '克' });
};

const removeIngredient = (index) => {
  formState.ingredientList.splice(index, 1);
};

const addStep = () => {
  formState.cookingSteps.push({ content: '' });
};

const removeStep = (index) => {
  formState.cookingSteps.splice(index, 1);
};

const onFinish = async () => {
  try {
    // 格式化食材列表
    const ingredients = formState.ingredientList
      .map(item => `${item.name} ${item.amount}${item.unit}`)
      .join('\n');

    // 格式化烹饪步骤
    const instructions = formState.cookingSteps
      .map((step, index) => `${index + 1}. ${step.content}`)
      .join('\n');

    const response = await axios.post('http://localhost:5000/recipes/add', {
      title: formState.title,
      ingredients,
      instructions
    }, {
      withCredentials: true
    });

    if (response.status === 201) {
      message.success('菜谱添加成功！');
      // 修改跳转逻辑，延迟跳转确保数据更新
      setTimeout(() => {
        router.push('/recipes-view');  // 修改为正确的菜谱列表页面路由
      }, 1000);
    }
  } catch (error) {
    console.error('添加失败:', error);
    message.error('添加失败：' + (error.response?.data?.message || '未知错误'));
  }
};
</script>

<style scoped>
.recipe-form {
  max-width: 1000px;
  margin: 40px auto;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #42b983;
}
</style>
