<template>
    <div class="ingredient-list">
        <h2>我的食品柜</h2>
        <a-table :columns="columns" :data-source="ingredients" :loading="loading">
            <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'action'">
                    <a-space>
                        <a-button type="primary" size="small" @click="editIngredient(record)">编辑</a-button>
                        <a-button type="danger" size="small" @click="deleteIngredient(record.id)">删除</a-button>
                    </a-space>
                </template>
            </template>
        </a-table>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import eventBus from '../utils/eventBus.js';

const columns = [
    { title: '食材名称', dataIndex: 'name', key: 'name' },
    { title: '类别', dataIndex: 'category', key: 'category' },
    { title: '数量', dataIndex: 'quantity', key: 'quantity' },
    { title: '保质期', dataIndex: 'shelf_life', key: 'shelf_life' },
    { title: '购买日期', dataIndex: 'purchase_date', key: 'purchase_date' },
    { title: '操作', key: 'action' }
];
const ingredients = ref([]);
const loading = ref(false);

const fetchIngredients = async () => {
    loading.value = true;
    try {
        const response = await axios.get('http://localhost:5000/ingredient/get_all', {
            withCredentials: true
        });
        // 确保后端返回的数据是数组
        ingredients.value = Array.isArray(response.data) ? response.data : [];
    } catch (error) {
        console.error('Failed to fetch ingredients:', error);
    } finally {
        // 无论请求成功还是失败，都将 loading 状态更新为 false
        loading.value = false;
    }
};

const deleteIngredient = async (id) => {
    try {
        await axios.delete(`http://localhost:5000/ingredient/delete/${id}`);
        fetchIngredients();
    } catch (error) {
        console.error('Failed to delete ingredient:', error);
    }
};

const editIngredient = (record) => {
    // 这里可以实现编辑逻辑
    console.log('编辑食材:', record);
};

const handleIngredientAdded = () => {
    fetchIngredients();
};

onMounted(() => {
    eventBus.on('ingredientAdded', handleIngredientAdded);
    fetchIngredients();
});

onUnmounted(() => {
    eventBus.off('ingredientAdded', handleIngredientAdded);
});
</script>

<style scoped>
.ingredient-list {
    margin: 20px;
}
</style>