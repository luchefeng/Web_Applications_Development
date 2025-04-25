<template>
    <div class="ingredient-management">
        <h2>食品柜管理</h2>
        <a-form :model="ingredientData" @finish="addIngredient" @finishFailed="onFinishFailed">
            <!-- 食物名称 -->
            <a-form-item label="食物名称" name="name" :rules="[{ required: true, message: '请输入食物名称！' }]">
                <a-input v-model:value="ingredientData.name" />
            </a-form-item>

            <!-- 类别 -->
            <a-form-item label="类别" name="category" :rules="[{ required: true, message: '请选择类别！' }]">
                <a-select v-model:value="ingredientData.category">
                    <a-select-option value="主食">主食</a-select-option>
                    <a-select-option value="蔬菜">蔬菜</a-select-option>
                    <a-select-option value="肉类">肉类</a-select-option>
                    <a-select-option value="调料">调料</a-select-option>
                    <a-select-option value="水果">水果</a-select-option>
                    <a-select-option value="其他">其他</a-select-option>
                </a-select>
            </a-form-item>

            <!-- 保质期 -->
            <a-form-item label="保质期 (天)" name="shelf_life" :rules="[{ required: true, message: '请输入保质期！' }]">
                <a-input-number v-model:value="ingredientData.shelf_life" :min="1" />
            </a-form-item>

            <!-- 食物数量 -->
            <a-form-item label="食物数量" name="quantityValue" :rules="[{ required: true, message: '请输入食物数量！' }]">
                <div style="display: flex; gap: 10px;">
                    <!-- 数值输入 -->
                    <a-input-number v-model:value="ingredientData.quantityValue" :min="0" placeholder="数值" style="flex: 1;" />
                    <!-- 单位选择 -->
                    <a-select v-model:value="ingredientData.quantityUnit" style="width: 100px;">
                        <a-select-option value="jin">斤</a-select-option>
                        <a-select-option value="g">克</a-select-option>
                        <a-select-option value="kg">千克</a-select-option>
                        <a-select-option value="ml">毫升</a-select-option>
                        <a-select-option value="l">升</a-select-option>
                    </a-select>
                </div>
            </a-form-item>

            <!-- 自动转换成克 -->
            <a-form-item label="换算为克 (g)">
                <a-input v-model:value="ingredientData.quantityInGrams" disabled />
            </a-form-item>

            <!-- 单位卡路里 -->
            <a-form-item label="单位卡路里数目" name="unit_calories" :rules="[{ required: true, message: '请输入单位卡路里数目！' }]">
                <a-input-number v-model:value="ingredientData.unit_calories" :min="0" />
            </a-form-item>

            <!-- 购买日期 -->
            <a-form-item label="购买日期" name="purchase_date" :rules="[{ required: true, message: '请选择购买日期！' }]">
                <a-date-picker v-model:value="ingredientData.purchase_date" />
            </a-form-item>

            <a-form-item>
                <a-button type="primary" html-type="submit">添加食材</a-button>
            </a-form-item>
        </a-form>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import dayjs from 'dayjs';
import eventBus from '../utils/eventBus.js';

// 定义单位换算规则（以克为基础）
const unitToGrams = {
    g: 1,
    kg: 1000,
    ml: 1,     // 假设液体密度近似为1g/ml，可根据不同食物微调
    l: 1000,
    jin: 500
};

const ingredientData = ref({
    name: '',
    category: '',
    shelf_life: null,
    quantityValue: null,
    quantityUnit: 'jin',
    quantityInGrams: 0,   // 自动转换后的克数
    unit_calories: null,
    purchase_date: null
});

const successMessage = ref('');
const errorMessage = ref('');

const defaultShelfLifeMap = {
    '主食': 5,
    '水果': 7,
    '蔬菜': 5,
    '肉类': 3,
    '调料': 30,
    '其他': 15
};

watch(() => ingredientData.value.category, (newCategory) => {
    if (newCategory && defaultShelfLifeMap[newCategory] !== undefined) {
        ingredientData.value.shelf_life = defaultShelfLifeMap[newCategory];
    }
});

// 自动换算成克（g）
watch(
    () => [ingredientData.value.quantityValue, ingredientData.value.quantityUnit],
    ([newValue, newUnit]) => {
        const multiplier = unitToGrams[newUnit] || 1;
        ingredientData.value.quantityInGrams = newValue ? Math.round(newValue * multiplier) : 0;
    }
);

const formatDate = (date) => {
    return date ? dayjs(date).format('YYYY-MM-DD') : null;
};

const getUserId = () => {
    const userId = localStorage.getItem('user_id');
    if (userId === null || userId === 'undefined') {
        return null;
    }
    return userId;
};

const addIngredient = async () => {
    const user_id = getUserId();
    if (!user_id) {
        errorMessage.value = '未找到有效的 user_id，请先登录';
        return;
    }

    try {
        const data = {
            name: ingredientData.value.name,
            category: ingredientData.value.category,
            shelf_life: ingredientData.value.shelf_life,
            quantity: ingredientData.value.quantityInGrams,  // 最终传递克单位值
            unit_calories: ingredientData.value.unit_calories,
            purchase_date: formatDate(ingredientData.value.purchase_date),
            user_id: user_id
        };

        await axios.post('http://localhost:5000/ingredient/add', data, { withCredentials: true });
        successMessage.value = '食材添加成功！';
        errorMessage.value = '';
        eventBus.emit('ingredientAdded');
    } catch (error) {
        console.error('Failed to add ingredient:', error);
        errorMessage.value = '食材添加失败，请稍后再试。';
        successMessage.value = '';
    }
};

const onFinishFailed = (errorInfo) => {
    console.log('提交失败:', errorInfo);
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