<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <ElTabs v-model="activeName">
      <template v-for="item in tabs" :key="item.id">
        <ElTabPane v-if="!item.hidden" :name="item.tab_name" :label="item.tab_label">
          <ActivationCode v-if="item.tab_name === '注册|激活码管理'" />
          <ActivationRecords v-else-if="item.tab_name === '使用记录'" />
        </ElTabPane>
      </template>
    </ElTabs>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, h } from 'vue'
import { ElTabs, ElTabPane } from 'element-plus'
import ActivationCode from './components/ActivationCode.vue'
import ActivationRecords from './components/ActivationRecords.vue'

const activeName = ref('注册|激活码管理')

const tabs = ref([])

tabs.value = [
  { id: 1, tab_name: '注册|激活码管理', tab_label: '注册|激活码管理', hidden: false },
  { id: 2, tab_name: '使用记录', tab_label: '使用记录', hidden: false }
]
</script>
