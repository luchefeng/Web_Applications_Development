<template>
    <div class="ingredient-management">
      <h2>食品櫃管理</h2>
      <a-form :model="ingredientData" @finish="addIngredient" @finishFailed="onFinishFailed">
        <a-form-item label="食物名稱" name="name" :rules="[{ required: true, message: '請輸入食物名稱！' }]">
          <a-input v-model:value="ingredientData.name" />
        </a-form-item>
        <a-form-item label="類別" name="category" :rules="[{ required: true, message: '請選擇類別！' }]">
          <a-select v-model:value="ingredientData.category">
            <a-select-option value="蔬菜">蔬菜</a-select-option>
            <a-select-option value="肉類">肉類</a-select-option>
            <a-select-option value="調料">調料</a-select-option>
            <a-select-option value="其他">其他</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="保質期 (天)" name="shelf_life" :rules="[{ required: true, message: '請輸入保質期！' }]">
          <a-input-number v-model:value="ingredientData.shelf_life" :min="1" />
        </a-form-item>
        <a-form-item label="食物數量" name="quantity" :rules="[{ required: true, message: '請輸入食物數量！' }]">
          <a-input v-model:value="ingredientData.quantity" placeholder="例：1顆, 100g" />
        </a-form-item>
        <a-form-item label="單位卡路里數目" name="unit_calories" :rules="[{ required: true, message: '請輸入單位卡路里數目！' }]">
          <a-input-number v-model:value="ingredientData.unit_calories" :min="0" />
        </a-form-item>
        <a-form-item label="購買日期" name="purchase_date" :rules="[{ required: true, message: '請選擇購買日期！' }]">
          <a-date-picker v-model:value="ingredientData.purchase_date" />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">添加食材</a-button>
        </a-form-item>
      </a-form>
      <div v-if="ingredients.length">
        <h3>食品櫃列表</h3>
        <ul>
          <li v-for="ingredient in ingredients" :key="ingredient.id">
            {{ ingredient.name }} - {{ ingredient.category }} - {{ ingredient.quantity }}
          </li>
        </ul>
      </div>
      <!-- 顯示錯誤和成功消息 -->
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const ingredientData = ref({
    name: '',
    category: '',
    shelf_life: null,
    quantity: '',
    unit_calories: null,
    purchase_date: null
  });
  
  const ingredients = ref([]);
  const successMessage = ref('');
  const errorMessage = ref('');
  
  const fetchIngredients = async () => {
    try {
      const response = await axios.get('http://localhost:5000/ingredient/get_all');
      ingredients.value = response.data;
    } catch (error) {
      console.error('Failed to fetch ingredients:', error);
    }
  };
  
  const addIngredient = async () => {
    try {
      const data = {
        ...ingredientData.value,
        purchase_date: ingredientData.value.purchase_date.format('YYYY-MM-DD')
      };
      await axios.post('http://localhost:5000/ingredient/add', data, { withCredentials: true });
      successMessage.value = '食材添加成功！';
      errorMessage.value = '';
      fetchIngredients();
    } catch (error) {
      console.error('Failed to add ingredient:', error);
      errorMessage.value = '食材添加失敗，請稍後再試。';
      successMessage.value = '';
    }
  };
  
  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };
  
  onMounted(() => {
    fetchIngredients();
  });
  </script>
  
  <style scoped>
  .ingredient-management {
    max-width: 600px;
    margin: auto;
    padding: 20px;
  }
  
  .error {
    color: red;
  }
  
  .success {
    color: green;
  }
  </style>
  