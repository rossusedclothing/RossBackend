<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <ElTabs v-model="activeName">
      <template v-for="item in tabs" :key="item.id">
        <ElTabPane v-if="!item.hidden" :name="item.tab_name" :label="item.tab_label">
          <Clothing v-if="item.tab_name === '服装'" />
          <Electric v-else-if="item.tab_name === '电动车'" />
        </ElTabPane>
      </template>
    </ElTabs>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, h } from 'vue'
import { ElTabs, ElTabPane } from 'element-plus'
import Clothing from './components/Clothing/Clothing.vue'
import Electric from './components/Electric/Electric.vue'

const activeName = ref('服装')

const tabs = ref([])

tabs.value = [
  { id: 1, tab_name: '服装', tab_label: '服装', hidden: false },
  { id: 2, tab_name: '电动车', tab_label: '电动车', hidden: false },
  { id: 3, tab_name: '家居用品', tab_label: '家居用品', hidden: true }
]
</script>
