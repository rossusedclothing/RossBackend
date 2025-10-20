<template>
  <div class="p-4">
    <div class="flex justify-between mb-4">
      <div>
        <el-input
          v-model="filters.app_name"
          placeholder="搜索 app 名称"
          clearable
          @keyup.enter="onSearch"
        />
        <el-button @click="onSearch" type="primary" plain>搜索</el-button>
      </div>
      <div>
        <el-button type="primary" @click="openCreate">新增更新</el-button>
      </div>
    </div>

    <el-table :data="list" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="app_name" label="App 名称" />
      <el-table-column prop="version" label="版本" />
      <el-table-column prop="desc" label="描述" />
      <el-table-column label="操作" width="240">
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
        :page-size="paging.limit"
        :total="paging.total"
        layout="prev, pager, next"
        @current-change="onPageChange"
      />
    </div>

    <el-dialog :title="dialogTitle" v-model="showDialog" width="700px">
      <el-form :model="form">
        <el-form-item label="App 名称">
          <el-input v-model="form.app_name" />
        </el-form-item>
        <el-form-item label="版本">
          <el-input v-model="form.version" />
        </el-form-item>
        <el-form-item label="更新 JSON">
          <el-input
            type="textarea"
            :rows="8"
            v-model="form.update_json"
            placeholder="放入 JSON 字符串或结构"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            autosize
            :rows="5"
            type="textarea"
            placeholder="Please input"
            v-model="form.desc"
          />
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
  ElMessage,
} from 'element-plus'
import {
  getAppUpdateListApi,
  addAppUpdateApi,
  updateAppUpdateApi,
  delAppUpdateApi,
  getAppUpdateDetailApi,
} from '@/api/bot/panel/panel'

const list = ref<any[]>([])
const paging = reactive({ page: 1, limit: 10, total: 0, v_order: 'desc' })
const filters = reactive({ app_name: '' })
const showDialog = ref(false)
const dialogTitle = ref('新增更新')
const isEdit = ref(false)
const editId = ref<number | null>(null)
const form = reactive({ app_name: '', version: '', update_json: '', desc: '' })

const load = async () => {
  const res: any = await getAppUpdateListApi({
    ...paging,
    ...filters,
  })
  if (res?.data) {
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
  dialogTitle.value = '新增更新'
  Object.assign(form, { app_name: '', version: '', update_json: '', desc: '' })
  showDialog.value = true
}
const onEdit = async (row: any) => {
  isEdit.value = true
  editId.value = row.id
  dialogTitle.value = '编辑更新'
  const res: any = await getAppUpdateDetailApi(row.id)
  if (res?.data) Object.assign(form, res.data)
  showDialog.value = true
}
const onView = (row: any) => {
  ElMessageBox.alert(JSON.stringify(row, null, 2), '详情')
}
const onSubmit = async () => {
  try {
    await (isEdit.value ? updateAppUpdateApi(editId.value as number, form) : addAppUpdateApi(form))
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
      await delAppUpdateApi([row.id])
      ElMessage({ message: '删除成功', type: 'success' })
      load()
    })
    .catch(() => {})
}
</script>
