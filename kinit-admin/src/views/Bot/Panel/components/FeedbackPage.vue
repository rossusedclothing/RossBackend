<template>
  <div class="p-4">
    <div class="flex justify-between mb-4">
      <div class="flex gap-2">
        <el-input
          v-model="filters.app_name"
          placeholder="按 app 名称搜索"
          clearable
          @keyup.enter="onSearch"
        />
        <el-button @click="onSearch" type="primary" plain>搜索</el-button>
      </div>
      <div>
        <el-button type="primary" @click="openCreate">新增反馈</el-button>
      </div>
    </div>

    <el-table :data="list" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="app_name" label="App 名称" />
      <el-table-column prop="text" label="反馈内容" />
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="onView(scope.row)">查看</el-button>
          <el-button size="small" type="primary" @click="onEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="onDel(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="mt-4 flex justify-end">
      <el-pagination
        :current-page="paging.page"
        :page-size="paging.pageSize"
        :total="paging.total"
        layout="prev, pager, next"
        @current-change="onPageChange"
      />
    </div>

    <el-dialog :title="dialogTitle" v-model="showDialog">
      <el-form :model="form">
        <el-form-item label="App 名称">
          <el-input v-model="form.app_name" />
        </el-form-item>
        <el-form-item label="反馈">
          <el-input v-model="form.text" type="textarea" rows="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="onSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import {
  ElButton,
  ElInput,
  ElTable,
  ElTableColumn,
  ElDialog,
  ElForm,
  ElFormItem,
  ElPagination,
  ElMessageBox,
  ElMessage
} from 'element-plus'
import {
  getFeedbackListApi,
  addFeedbackApi,
  updateFeedbackApi,
  delFeedbackApi,
  getFeedbackDetailApi
} from '@/api/bot/panel/panel'

const list = ref<any[]>([])
const paging = reactive({ page: 1, pageSize: 10, total: 0 })
const filters = reactive({ app_name: '' })

const showDialog = ref(false)
const dialogTitle = ref('新增反馈')
const isEdit = ref(false)
const editId = ref<number | null>(null)
const form = reactive({ app_name: '', text: '' })

const load = async () => {
  const res: any = await getFeedbackListApi({
    page: paging.page,
    pageSize: paging.pageSize,
    ...filters
  })
  if (res && res.data) {
    list.value = res.data || []
    paging.total = res.data.total || list.value.length
  }
}

onMounted(load)
const onSearch = () => {
  paging.page = 1
  load()
}
const onPageChange = (p: number) => {
  paging.page = p
  load()
}

const openCreate = () => {
  isEdit.value = false
  editId.value = null
  dialogTitle.value = '新增反馈'
  Object.assign(form, { app_name: '', text: '' })
  showDialog.value = true
}
const onEdit = async (row: any) => {
  isEdit.value = true
  editId.value = row.id
  dialogTitle.value = '编辑反馈'
  const res: any = await getFeedbackDetailApi(row.id)
  if (res?.data) Object.assign(form, res.data)
  showDialog.value = true
}
const onView = (row: any) => {
  ElMessageBox.alert(row.text || '-', '反馈内容')
}
const onSubmit = async () => {
  try {
    await (isEdit.value ? updateFeedbackApi(editId.value as number, form) : addFeedbackApi(form))
    ElMessage({ message: '保存成功', type: 'success' })
    showDialog.value = false
    load()
  } catch {
    ElMessage({ message: '保存失败', type: 'error' })
  }
}
const onDel = (row: any) => {
  ElMessageBox.confirm('确认删除？', '提示')
    .then(async () => {
      await delFeedbackApi([row.id])
      ElMessage({ message: '删除成功', type: 'success' })
      load()
    })
    .catch(() => {})
}
</script>
