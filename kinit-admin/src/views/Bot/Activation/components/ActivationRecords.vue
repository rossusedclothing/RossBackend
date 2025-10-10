<template>
  <div class="p-6">
    <div class="flex justify-between mb-4">
      <h2 class="text-xl font-semibold">使用记录</h2>
      <el-button type="success" @click="loadData">刷新</el-button>
    </div>

    <el-table :data="tableData" border v-loading="loading" class="rounded-lg shadow">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="code_id" label="激活码ID" width="120" />
      <el-table-column prop="user_id" label="用户ID" />
      <el-table-column prop="device_id" label="设备ID" />
      <el-table-column prop="ip_address" label="IP地址" width="160" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column prop="last_verified_datetime" label="最后验证时间" />
    </el-table>
    <el-pagination
      size="small"
      layout="prev, pager, next"
      :total="50"
      @next-click="
        (val) => {
          searchForm.page = val
          loadData()
        }
      "
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getActivationRecords } from '@/api/bot/activationcode/activationcode'
import { ElButton, ElPagination, ElTable, ElTableColumn } from 'element-plus'

const tableData = ref<any[]>([])
const loading = ref(false)
const searchForm = ref({
  page: 1,
  limit: 10,
  v_order: 'desc',
  v_order_field: undefined
})
const total = ref(0)

const loadData = async () => {
  loading.value = true
  try {
    const params = Object.assign(searchForm.value, {})
    const res = await getActivationRecords(params)
    tableData.value = res.data || []
    total.value = res.data?.length || 0
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>
