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
import CustomerInfo from './components/CustomerInfo.vue'
import CustomerMessage from './components/CustomerMessage.vue'
import SalesAgentConfig from './components/SalesAgentConfig.vue'
import SalesAgentWorkflow from '@/views/Customer/components/SalesAgentWorkflow.vue'

// 响应式数据
const activeTab = ref('CustomerInfo')

// 标签页配置
const tabs = [
  {
    name: 'CustomerInfo',
    label: '客户信息',
    component: CustomerInfo,
    hidden: false
  },
  {
    name: 'CustomerMessage',
    label: '客户消息记录',
    component: CustomerMessage,
    hidden: false
  },
  {
    name: 'SalesAgentConfig',
    label: '业务员配置',
    component: SalesAgentConfig,
    hidden: false
  },
  {
    name: 'SalesAgentWorkflow',
    label: '工作流配置',
    component: SalesAgentWorkflow,
    hidden: false
  }
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
