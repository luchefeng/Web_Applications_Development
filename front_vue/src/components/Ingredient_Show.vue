<template>
    <div class="ingredient-list">
        <h2>我的食品柜</h2>
        <a-table :columns="columns" :data-source="ingredients" :loading="loading">
            <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'action'">
                    <a-space>
                        <a-button type="primary" size="small" @click="openEditModal(record)">编辑</a-button>
                        <a-button type="danger" size="small" @click="confirmDelete(record.id)">删除</a-button>
                    </a-space>
                </template>
            </template>
        </a-table>
        <!-- 编辑模态框 -->
        <a-modal
            title="编辑食材信息"
            :visible="editModalVisible"
            @ok="handleEditOk"
            @cancel="handleEditCancel"
        >
            <a-form :model="editIngredientData" @finish="handleEditOk" @finishFailed="onFinishFailed">
                <a-form-item label="食物名稱" name="name" :rules="[{ required: true, message: '請輸入食物名稱！' }]">
                    <a-input v-model:value="editIngredientData.name" />
                </a-form-item>
                <a-form-item label="類別" name="category" :rules="[{ required: true, message: '請選擇類別！' }]">
                    <a-select v-model:value="editIngredientData.category">
                        <a-select-option value="蔬菜">蔬菜</a-select-option>
                        <a-select-option value="肉類">肉類</a-select-option>
                        <a-select-option value="調料">調料</a-select-option>
                        <a-select-option value="其他">其他</a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item label="保質期 (天)" name="shelf_life" :rules="[{ required: true, message: '請輸入保質期！' }]">
                    <a-input-number v-model:value="editIngredientData.shelf_life" :min="1" />
                </a-form-item>
                <a-form-item label="食物數量" name="quantity" :rules="[{ required: true, message: '請輸入食物數量！' }]">
                    <a-input v-model:value="editIngredientData.quantity" placeholder="例：1顆, 100g" />
                </a-form-item>
                <a-form-item label="單位卡路里數目" name="unit_calories" :rules="[{ required: true, message: '請輸入單位卡路里數目！' }]">
                    <a-input-number v-model:value="editIngredientData.unit_calories" :min="0" />
                </a-form-item>
                <a-form-item label="購買日期" name="purchase_date" :rules="[{ required: true, message: '請選擇購買日期！' }]">
                    <a-date-picker v-model:value="editIngredientData.purchase_date" />
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import eventBus from '../utils/eventBus.js';
import { Modal } from 'ant-design-vue';
import dayjs from 'dayjs';
import { Tooltip } from 'ant-design-vue';
import { h } from 'vue';

const columns = [
    { title: '食材名称', dataIndex: 'name', key: 'name' },
    { title: '类别', dataIndex: 'category', key: 'category' },
    { title: '数量（g）', dataIndex: 'quantity', key: 'quantity', align: 'center' },
    { title: '单位卡路里（kcal/100g）', dataIndex: 'unit_calories', key: 'unit_calories', align: 'center' },
    {
        title: '总卡路里（kcal）',
        key: 'total_calories',
        align: 'center',  // 添加这个属性
        customRender: ({ record }) => {
            const quantityNumber = parseFloat(record.quantity);
            if (isNaN(quantityNumber)) {
                return '无法计算';
            }
            // 正确计算：数量(g) / 100 × 单位卡路里(kcal/100g)
            const totalCalories = (quantityNumber / 100) * record.unit_calories;
            return Math.round(totalCalories);  // 取整，不保留小数
        }
    },
    { title: '保质期（天）', dataIndex: 'shelf_life', key: 'shelf_life', align: 'center' },
    { title: '购买日期', dataIndex: 'purchase_date', key: 'purchase_date', align: 'center' },
    {
        title: '过期时间',
        dataIndex: 'expiry_date',
        key: 'expiry_date',
        align: 'center',  // 添加这个属性
        customRender: ({ text, record }) => {
            const today = dayjs();
            const expiry = dayjs(text);
            const diff = expiry.diff(today, 'day');
            let color = 'inherit';
            let tooltipText = null;

            if (diff < 0) {
                color = 'gray';
                tooltipText = '已過期';
            } else if (diff <= 2) {
                color = 'red';
                tooltipText = '即將過期';
            }

            return tooltipText
                ? h(Tooltip, { title: tooltipText }, {
                    default: () => h('span', { style: `color: ${color}` }, text)
                })
                : h('span', { style: `color: ${color}` }, text);
        }
    },
    { title: '操作', key: 'action', align: 'center' },
];
const ingredients = ref([]);
const loading = ref(false);
const editModalVisible = ref(false);
const editIngredientData = ref({
    id: null,
    name: '',
    category: '',
    shelf_life: null,
    quantity: '',
    unit_calories: null,
    purchase_date: null
});

const fetchIngredients = async () => {
    loading.value = true;
    try {
        const response = await axios.get('http://localhost:5000/ingredient/get_all', {
            withCredentials: true
        });
        const rawData = Array.isArray(response.data) ? response.data : [];

        // ✅ 计算过期时间
        ingredients.value = rawData.map(item => {
            const purchaseDate = dayjs(item.purchase_date);
            const expiryDate = item.shelf_life
                ? purchaseDate.add(item.shelf_life, 'day').format('YYYY-MM-DD')
                : '未知';
            return {
                ...item,
                expiry_date: expiryDate
            };
        });
    } catch (error) {
        console.error('Failed to fetch ingredients:', error);
    } finally {
        loading.value = false;
    }
};

const deleteIngredient = async (id) => {
    console.log('要删除的食材 id:', id);
    try {
        const response = await axios.delete(`http://localhost:5000/ingredient/delete/${id}`, {
            withCredentials: true
        });
        console.log('删除请求响应:', response);
        if (response.status === 200 && response.data.message === 'Ingredient deleted successfully!') {
            ingredients.value = ingredients.value.filter(item => item.id !== id);
        } else {
            console.error('删除失败，响应状态码:', response.status);
            console.error('删除失败，响应消息:', response.data.message);
        }
    } catch (error) {
        console.error('Failed to delete ingredient:', error);
    }
};

const confirmDelete = (id) => {
    Modal.confirm({
        title: '确认删除',
        content: '你确定要删除这条食材记录吗？',
        onOk() {
            deleteIngredient(id);
        },
        onCancel() {
            console.log('用户取消删除操作');
        },
    });
};

const openEditModal = (record) => {
    editIngredientData.value = { ...record };
    editIngredientData.value.purchase_date = dayjs(record.purchase_date);
    editModalVisible.value = true;
};

const handleEditOk = async () => {
    try {
        const data = {
            ...editIngredientData.value,
            purchase_date: dayjs(editIngredientData.value.purchase_date).format('YYYY-MM-DD')
        };
        const response = await axios.put(`http://localhost:5000/ingredient/update/${editIngredientData.value.id}`, data, {
            withCredentials: true
        });
        if (response.status === 200) {
            // 更新前端列表
            const index = ingredients.value.findIndex(item => item.id === editIngredientData.value.id);
            if (index !== -1) {
                ingredients.value[index] = { ...editIngredientData.value };
                ingredients.value[index].purchase_date = dayjs(editIngredientData.value.purchase_date).format('YYYY-MM-DD');
                const expiryDate = dayjs(editIngredientData.value.purchase_date).add(editIngredientData.value.shelf_life, 'day').format('YYYY-MM-DD');
                ingredients.value[index].expiry_date = expiryDate;
            }
            editModalVisible.value = false;
        } else {
            console.error('编辑失败，响应状态码:', response.status);
        }
    } catch (error) {
        console.error('Failed to edit ingredient:', error);
    }
};

const handleEditCancel = () => {
    editModalVisible.value = false;
};

const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
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