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
import { ref } from 'vue';
import axios from 'axios';

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

// 从父组件接收刷新方法
defineExpose({
  refreshList: fetchIngredients
});

async function fetchIngredients() {
  loading.value = true;
  try {
    const response = await axios.get('http://localhost:5000/ingredient/get_all');
    ingredients.value = response.data;
  } catch (error) {
    console.error('Failed to fetch ingredients:', error);
  }
  loading.value = false;
}

async function deleteIngredient(id) {
  try {
    await axios.delete(`http://localhost:5000/ingredient/delete/${id}`);
    fetchIngredients();
  } catch (error) {
    console.error('Failed to delete ingredient:', error);
  }
}
</script>

<style scoped>
.ingredient-list {
  margin: 20px;
}
</style>
