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
import ApiKeysPage from './components/ApiKeysPage.vue'
import AppUpdate from './components/AppUpdate.vue'
import FeedbackPage from './components/FeedbackPage.vue'

// 响应式数据
const activeTab = ref('apiKeys')

// 标签页配置
const tabs = [
  {
    name: 'apiKeys',
    label: 'API密钥管理',
    component: ApiKeysPage,
    hidden: false
  },
  {
    name: 'appUpdate',
    label: '应用更新',
    component: AppUpdate,
    hidden: false
  },
  {
    name: 'feedback',
    label: '用户反馈',
    component: FeedbackPage,
    hidden: false // 可以根据需要显示/隐藏
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
