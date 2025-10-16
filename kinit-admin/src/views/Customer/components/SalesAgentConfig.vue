<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-2">
        <el-input
          v-model="filters.keyword"
          placeholder="搜索姓名或手机号"
          clearable
          @clear="onSearch"
          @keydown.enter="onSearch"
        />
        <el-button :plain="true" @click="onSearch">搜索</el-button>
        <el-button type="primary" @click="onOpenCreate">创建配置</el-button>
      </div>
      <div class="text-sm text-gray-500">总数：{{ paging.total }}</div>
    </div>

    <el-table :data="list" stripe style="width: 100%" :empty-text="'暂无数据'">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="config" label="配置" show-overflow-tooltip />

      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button size="small" @click="onView(scope.row)">查看</el-button>
          <el-button size="small" type="primary" @click="onEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="onDel(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="mt-4 flex justify-end">
      <el-pagination
        background
        layout="prev, pager, next, sizes, total"
        :page-size="paging.limit"
        :current-page="paging.page"
        :page-sizes="[10, 20, 50, 100]"
        :total="paging.total"
        @size-change="onLimitChange"
        @current-change="onPageChange"
      />
    </div>

    <!-- 查看弹窗 -->
    <el-dialog
      v-model="viewDialog.visible"
      width="640px"
      :title="'业务员配置 - ' + (viewDialog.data?.name || '')"
    >
      <div class="space-y-2">
        <div><strong>名称：</strong>{{ viewDialog.data?.name }}</div>
        <div><strong>手机号：</strong>{{ viewDialog.data?.phone }}</div>
        <div><strong>描述：</strong></div>
        <el-input type="textarea" :rows="3" :model-value="viewDialog.data?.description" disabled />
        <div><strong>配置：</strong></div>
        <el-input type="textarea" :rows="6" :model-value="viewDialog.data?.config" disabled />
      </div>
      <template #footer>
        <el-button @click="viewDialog.visible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="editDialog.visible"
      width="700px"
      :title="editDialog.isEdit ? '编辑配置' : '创建配置'"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="space-y-2">
        <el-form-item label="名称" prop="name"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="手机号" prop="phone"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="描述" prop="description"
          ><el-input type="textarea" :rows="3" v-model="form.description"
        /></el-form-item>
        <el-form-item label="配置(JSON或文本)" prop="config">
          <el-input type="textarea" :rows="8" v-model="form.config" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="onCloseEdit">取消</el-button>
        <el-button type="primary" @click="onSubmitForm">{{
          editDialog.isEdit ? '保存' : '创建'
        }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

// Element Plus 组件显式导入
import {
  ElTable,
  ElTableColumn,
  ElButton,
  ElPagination,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElMessageBox,
  ElMessage,
} from 'element-plus'

// API
import {
  getSalesAgentConfigListApi,
  createSalesAgentConfigApi,
  updateSalesAgentConfigApi,
  deleteSalesAgentConfigApi,
  getSalesAgentConfigInfoApi,
} from '@/api/bot/customer/customer'

interface AgentConfig {
  id: number
  phone?: string
  name?: string
  description?: string
  config?: string
}

// 分页
const paging = reactive({ page: 1, limit: 10, total: 0, v_order: 'desc' })

const list = ref<AgentConfig[]>([])
const filters = reactive({ keyword: '' })

const fetchList = async () => {
  const params = {
    page: paging.page,
    limit: paging.limit,
    keyword: filters.keyword,
    v_order: paging.v_order,
  }
  try {
    const res: any = await getSalesAgentConfigListApi(params)
    if (res && res.data) {
      list.value = res.data || []
      paging.total = res.data.total ?? 0
    } else {
      list.value = []
      paging.total = 0
    }
  } catch (e) {
    console.error(e)
    ElMessage.error('获取配置列表失败')
  }
}

const onSearch = () => {
  paging.page = 1
  fetchList()
}

const onPageChange = (page: number) => {
  paging.page = page
  fetchList()
}
const onLimitChange = (limit: number) => {
  paging.limit = limit
  paging.page = 1
  fetchList()
}

// view/edit/create/delete
const viewDialog = reactive({ visible: false, data: null as AgentConfig | null })
const editDialog = reactive({ visible: false, isEdit: false, data_id: 0 })
const formRef = ref()
const form = reactive({
  name: '',
  phone: '',
  description: '',
  config: '',
})
const rules = reactive({
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
})

const onView = (row: AgentConfig) => {
  if (row?.id) {
    getSalesAgentConfigInfoApi(row.id)
      .then((res: any) => {
        viewDialog.data = res?.data ?? row
        viewDialog.visible = true
      })
      .catch(() => {
        viewDialog.data = row
        viewDialog.visible = true
      })
  } else {
    viewDialog.data = row
    viewDialog.visible = true
  }
}

const onEdit = (row: AgentConfig) => {
  editDialog.isEdit = true
  editDialog.data_id = row.id
  form.name = row.name ?? ''
  form.phone = row.phone ?? ''
  form.description = row.description ?? ''
  form.config = row.config ?? ''
  editDialog.visible = true
}

const onOpenCreate = () => {
  editDialog.isEdit = false
  editDialog.data_id = 0
  form.name = ''
  form.phone = ''
  form.description = ''
  form.config = ''
  editDialog.visible = true
}

const onCloseEdit = () => {
  editDialog.visible = false
}

const onSubmitForm = () => {
  ;(formRef.value as any)?.validate?.(async (valid: boolean) => {
    if (!valid) return
    try {
      if (editDialog.isEdit && editDialog.data_id) {
        await updateSalesAgentConfigApi(editDialog.data_id, { ...form })
        ElMessage.success('更新成功')
      } else {
        await createSalesAgentConfigApi({ ...form })
        ElMessage.success('创建成功')
      }
      editDialog.visible = false
      fetchList()
    } catch (e) {
      ElMessage.error('操作失败')
    }
  })
}

const onDel = (row: AgentConfig) => {
  ElMessageBox.confirm('确认删除该配置吗？', '删除确认', { type: 'warning' })
    .then(async () => {
      try {
        await deleteSalesAgentConfigApi([row.id])
        ElMessage.success('删除成功')
        fetchList()
      } catch (e) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {})
}

onMounted(() => {
  fetchList()
})
</script>

<style scoped>
/* tailwind + 自定义样式可混合使用 */
</style>
