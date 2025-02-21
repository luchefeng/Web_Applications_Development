<template>
    <div class="ingredient-management">
        <h2>食品柜管理</h2>
        <a-form :model="ingredientData" @finish="addIngredient" @finishFailed="onFinishFailed">
            <a-form-item label="食物名称" name="name" :rules="[{ required: true, message: '请输入食物名称！' }]">
                <a-input v-model:value="ingredientData.name" />
            </a-form-item>
            <a-form-item label="类别" name="category" :rules="[{ required: true, message: '请选择类别！' }]">
                <a-select v-model:value="ingredientData.category">
                    <a-select-option value="蔬菜">蔬菜</a-select-option>
                    <a-select-option value="肉类">肉类</a-select-option>
                    <a-select-option value="调料">调料</a-select-option>
                    <a-select-option value="水果">水果</a-select-option>
                    <a-select-option value="其他">其他</a-select-option>
                </a-select>
            </a-form-item>
            <a-form-item label="保质期 (天)" name="shelf_life" :rules="[{ required: true, message: '请输入保质期！' }]">
                <a-input-number v-model:value="ingredientData.shelf_life" :min="1" />
            </a-form-item>
            <a-form-item label="食物数量" name="quantity" :rules="[{ required: true, message: '请输入食物数量！' }]">
                <a-input v-model:value="ingredientData.quantity" placeholder="例：1颗, 100g" />
            </a-form-item>
            <a-form-item label="单位卡路里数目" name="unit_calories" :rules="[{ required: true, message: '请输入单位卡路里数目！' }]">
                <a-input-number v-model:value="ingredientData.unit_calories" :min="0" />
            </a-form-item>
            <a-form-item label="购买日期" name="purchase_date" :rules="[{ required: true, message: '请选择购买日期！' }]">
                <a-date-picker v-model:value="ingredientData.purchase_date" />
            </a-form-item>
            <a-form-item>
                <a-button type="primary" html-type="submit">添加食材</a-button>
            </a-form-item>
        </a-form>
        <!-- 显示错误和成功消息 -->
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import eventBus from '../utils/eventBus.js';
import dayjs from 'dayjs';

const ingredientData = ref({
    name: '',
    category: '',
    shelf_life: null,
    quantity: '',
    unit_calories: null,
    purchase_date: null
});
const successMessage = ref('');
const errorMessage = ref('');

const formatDate = (date) => {
    return date? dayjs(date).format('YYYY-MM-DD') : null;
};

const getUserId = () => {
    const userId = localStorage.getItem('user_id');
    console.log('从 localStorage 获取的 user_id:', userId);
    if (userId === null || userId === 'undefined') {
        return null;
    }
    return userId;
};

const addIngredient = async () => {
    const user_id = getUserId();
    if (!user_id) {
        console.error('未找到有效的 user_id，请先登录');
        errorMessage.value = '未找到有效的 user_id，请先登录';
        return;
    }
    console.log('准备发送的 user_id:', user_id);
    try {
        const data = {
            ...ingredientData.value,
            purchase_date: formatDate(ingredientData.value.purchase_date),
            user_id: user_id
        };
        const response = await axios.post('http://localhost:5000/ingredient/add', data, { withCredentials: true });
        successMessage.value = '食材添加成功！';
        errorMessage.value = '';

        // 触发事件通知 Ingredient_Show.vue 更新
        eventBus.emit('ingredientAdded');
    } catch (error) {
        console.error('Failed to add ingredient:', error);
        if (error.response) {
            console.log('Response data:', error.response.data);
        }
        errorMessage.value = '食材添加失败，请稍后再试。';
        successMessage.value = '';
    }
};

const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};
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