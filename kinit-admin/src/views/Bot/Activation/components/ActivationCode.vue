<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">激活码管理</h2>
      <div class="space-x-2">
        <el-button type="primary" @click="openCreateDialog">新增</el-button>
        <el-button type="success" @click="loadData">刷新</el-button>
        <el-button type="danger" :disabled="!selectedIds.length" @click="handleDelete"
          >删除</el-button
        >
      </div>
    </div>

    <el-table
      :data="tableData"
      v-loading="loading"
      border
      @selection-change="handleSelectionChange"
      class="rounded-lg shadow"
    >
      <el-table-column type="selection" width="50" />
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="code" label="激活码" tooltipEffect width="100" />
      <el-table-column prop="type" label="类型" width="100" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column prop="user_limit" label="用户数限制" width="120" />
      <el-table-column prop="duration_days" label="有效天数" width="100" />
      <el-table-column prop="activated_by" label="激活人" />
      <el-table-column prop="activated_datetime" label="激活时间" />
      <el-table-column label="操作" width="160">
        <template #default="scope">
          <el-button size="small" type="primary" @click="editRow(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteRow(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="mt-4"
      background
      layout="prev, pager, next"
      :page-size="pageSize"
      :total="total"
      @current-change="loadData"
    />

    <el-dialog
      v-model="dialogVisible"
      :title="editMode ? '编辑激活码' : '新增激活码'"
      width="500px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="激活码">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="类型">
          <el-input v-model="form.type" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" placeholder="选择状态">
            <el-option label="未使用" value="unused" />
            <el-option label="已使用" value="used" />
            <el-option label="过期" value="expired" />
          </el-select>
        </el-form-item>
        <el-form-item label="用户限制">
          <el-input v-model="form.user_limit" />
        </el-form-item>
        <el-form-item label="有效天数">
          <el-input v-model="form.duration_days" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveData">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import {
  createActivationCode,
  deleteActivationCodes,
  getActivationCodes,
  updateActivationCode
} from '@/api/bot/activationcode/activationcode'
import {
  ElButton,
  ElDialog,
  ElInput,
  ElMessage,
  ElMessageBox,
  ElOption,
  ElSelect,
  ElFormItem,
  ElForm,
  ElPagination,
  ElTable,
  ElTableColumn
} from 'element-plus'

const tableData = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editMode = ref(false)
const selectedIds = ref<number[]>([])
const total = ref(0)
const pageSize = 10

const form = reactive({
  id: null,
  code: '',
  type: '',
  status: 'unused',
  user_limit: 1,
  duration_days: 30
})

const loadData = async () => {
  loading.value = true
  try {
    const res = await getActivationCodes()
    tableData.value = res.data || []
    total.value = res.data?.length || 0
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  editMode.value = false
  Object.assign(form, {
    id: null,
    code: '',
    type: '',
    status: 'unused',
    user_limit: 1,
    duration_days: 30
  })
  dialogVisible.value = true
}

const editRow = (row: any) => {
  editMode.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

const saveData = async () => {
  try {
    if (editMode.value && form.id) {
      await updateActivationCode(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createActivationCode(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async () => {
  ElMessageBox.confirm('确认删除选中的激活码吗？', '提示').then(async () => {
    await deleteActivationCodes(selectedIds.value)
    ElMessage.success('删除成功')
    loadData()
  })
}

const deleteRow = async (row: any) => {
  await deleteActivationCodes([row.id])
  ElMessage.success('删除成功')
  loadData()
}

const handleSelectionChange = (rows: any[]) => {
  selectedIds.value = rows.map((r) => r.id)
}

onMounted(loadData)
</script>
