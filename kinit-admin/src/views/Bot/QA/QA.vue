<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <ElTabs v-model="activeTab" type="card">
      <ElTabPane v-for="tab in visibleTabs" :key="tab.name" :name="tab.name" :label="tab.label">
        <component
          :is="tab.component"
          :tabParams="getTabParams(tab.name)"
          @switch-tab="handleSwitchTab"
        />
      </ElTabPane>
    </ElTabs>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { ElTabs, ElTabPane } from 'element-plus'
import Template from './components/Template/Template.vue'
import QAndA from './components/QAndA/QAndA.vue'

// 响应式数据
const activeTab = ref('Template')

// 存储各标签页的参数
const tabParams = reactive({
  Template: {},
  QAndA: {},
})

// 标签页配置
const tabs = [
  {
    name: 'Template',
    label: '问题模板',
    component: Template,
    hidden: false,
  },
  {
    name: 'QAndA',
    label: '问答详情',
    component: QAndA,
    hidden: false,
  },
]

// 计算属性：可见的标签页
const visibleTabs = computed(() => tabs.filter((tab) => !tab.hidden))

// 切换标签
const switchTab = (tabName, params = {}) => {
  activeTab.value = tabName
  if (params && Object.keys(params).length > 0) {
    tabParams[tabName] = { ...tabParams[tabName], ...params }
  }
}

// 获取标签页参数
const getTabParams = (tabName) => {
  return tabParams[tabName] || {}
}

// 处理子组件的切换事件
const handleSwitchTab = ({ tabName, params }) => {
  switchTab(tabName, params)
}

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
