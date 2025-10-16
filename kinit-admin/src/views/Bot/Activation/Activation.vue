<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <ElTabs v-model="activeTab" type="card">
      <ElTabPane v-for="tab in visibleTabs" :key="tab.name" :name="tab.name" :label="tab.label">
        <component :is="tab.component" />
      </ElTabPane>
    </ElTabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElTabs, ElTabPane } from 'element-plus'
import ActivationCode from './components/ActivationCode.vue'
import ActivationRecords from './components/ActivationRecords.vue'

// 响应式数据
const activeTab = ref('ActivationCode')

// 标签页配置
const tabs = [
  {
    name: 'ActivationCode',
    label: '注册|激活管理',
    component: ActivationCode,
    hidden: false,
  },
  {
    name: 'ActivationRecords',
    label: '使用记录',
    component: ActivationRecords,
    hidden: false,
  },
]

// 计算属性：可见的标签页
const visibleTabs = computed(() => tabs.filter((tab) => !tab.hidden))
</script>

<style scoped>
/* 可以添加一些自定义样式 */
:deep(.el-tabs__header) {
  margin-bottom: 20px;
}

:deep(.el-tabs__content) {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
