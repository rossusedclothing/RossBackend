<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">表单管理</h2>
      <div class="space-x-2">
        <!--        <el-button type="primary" @click="openCreateDialog">新增</el-button>-->
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
      <el-table-column fixed type="selection" width="50" />
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="code" label="客户名称" tooltipEffect width="100">
        <template #default="scope">
          <label
            style="
              display: -webkit-box;
              -webkit-line-clamp: 2;
              -webkit-box-orient: vertical;
              overflow: hidden;
              word-break: break-all;
            "
            >{{ scope.row.name }}</label
          >
        </template>
      </el-table-column>
      <el-table-column prop="position" label="职位" width="100" />
      <el-table-column prop="region" label="地区" width="100" />
      <el-table-column prop="factory_spec" label="公司规模" width="100" />
      <el-table-column prop="product" label="产品" width="100" />
      <el-table-column prop="website" label="网站链接" width="100" />
      <el-table-column prop="has_export_experience" label="有没有做过外贸" width="100">
        <template #default="scope">
          <label
            style="
              display: -webkit-box;
              -webkit-line-clamp: 2;
              -webkit-box-orient: vertical;
              overflow: hidden;
              word-break: break-all;
            "
            >{{ scope.row.has_export_experience == 1 ? '做过' : '未做过' }}</label
          >
        </template>
      </el-table-column>
      <el-table-column prop="export_market" label="产品出口市场" width="100" />
      <el-table-column prop="student_identity" label="学员身份" width="100" />
      <el-table-column prop="num_members_tradeteam" label="外贸团队人数" width="100" />
      <el-table-column prop="company_size" label="公司人数规模" width="100" />
      <el-table-column prop="create_datetime" label="表单创建时间" width="100" />
      <el-table-column prop="update_datetime" label="表单修改时间" width="100" />
      <el-table-column prop="is_delete" label="删除状态" width="100">
        <template #default="scope">
          <label
            style="
              display: -webkit-box;
              -webkit-line-clamp: 2;
              -webkit-box-orient: vertical;
              overflow: hidden;
              word-break: break-all;
            "
            >{{ scope.row.is_delete == 1 ? '已删除' : '未删除' }}</label
          >
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="160">
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
      :page-size="searchForm.limit"
      :total="total"
      @current-change="loadData"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { deleteRecord, getBusinessFormLists } from '@/api/businessform/list/list'
import {
  ElButton,
  ElMessage,
  ElMessageBox,
  ElPagination,
  ElTable,
  ElTableColumn,
} from 'element-plus'

const tableData = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editMode = ref(false)
const selectedIds = ref<number[]>([])
const total = ref(0)

const searchForm = reactive({
  page: 1,
  limit: 10,
  v_order: 'desc',
  v_order_field: undefined,
})

const form = reactive({
  id: null,
  code: '',
  type: 'trial',
  status: 'active',
  user_limit: 1,
  duration_days: 30,
})

const loadData = async () => {
  loading.value = true
  try {
    const params = Object.assign(searchForm, {})
    const res = await getBusinessFormLists(params)
    tableData.value = res.data || []
    total.value = res.data?.length || 0
  } finally {
    loading.value = false
  }
}

const editRow = (row: any) => {
  editMode.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

/*~~
        const saveData = async () => {
            try {
                if (editMode.value && form.id) {
                    await updateRecord(form.id, form)
                    ElMessage.success('更新成功')
                } else {
                    await createRecord(form)
                    ElMessage.success('创建成功')
                }
                dialogVisible.value = false
                loadData()
            } catch {
                ElMessage.error('操作失败')
            }
        }
        */

const handleDelete = async () => {
  ElMessageBox.confirm('确认删除选中的记录吗？', '提示').then(async () => {
    await deleteRecord(selectedIds.value)
    ElMessage.success('删除成功')
    loadData()
  })
}

const deleteRow = async (row: any) => {
  await deleteRecord([row.id])
  ElMessage.success('删除成功')
  loadData()
}

const handleSelectionChange = (rows: any[]) => {
  selectedIds.value = rows.map((r) => r.id)
}

// const generateCode = async () => {
//   const resp = await createGenerateCode()
//   if (resp.data && resp.data.length > 0) {
//     form.code = resp.data[0]
//   }
// }

onMounted(loadData)
</script>
