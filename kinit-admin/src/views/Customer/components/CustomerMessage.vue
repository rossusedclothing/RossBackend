<template>
  <div class="p-4">
    <!-- 顶部操作栏 -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-2">
        <el-input
          v-model="filters.keyword"
          placeholder="搜索客户名称或手机号"
          clearable
          @clear="onSearch"
          @keydown.enter="onSearch"
        />
        <el-button :plain="true" @click="onSearch">搜索</el-button>
        <el-button type="primary" @click="onOpenCreate">新增消息</el-button>
      </div>

      <div class="text-sm text-gray-500">总数：{{ paging.total }}</div>
    </div>

    <!-- 表格 -->
    <el-table :data="list" stripe style="width: 100%" :empty-text="'暂无数据'">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="customer_name" label="客户名称" />
      <el-table-column prop="customer_phone" label="手机号" />
      <el-table-column prop="customer_message" label="客户消息" show-overflow-tooltip />
      <el-table-column prop="receiver_message" label="回复消息" show-overflow-tooltip />

      <!-- 操作列 -->
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button size="small" @click="onView(scope.row)">查看</el-button>
          <el-button size="small" type="primary" @click="onEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="onDel(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
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

    <!-- 查看详情弹窗 -->
    <el-dialog
      v-model="viewDialog.visible"
      width="700px"
      :title="'消息详情 - ' + (viewDialog.data?.customer_name || '')"
    >
      <div class="space-y-3">
        <div><strong>客户名称：</strong>{{ viewDialog.data?.customer_name }}</div>
        <div><strong>手机号：</strong>{{ viewDialog.data?.customer_phone }}</div>
        <div><strong>客户消息：</strong></div>
        <el-input
          type="textarea"
          :rows="4"
          :model-value="viewDialog.data?.customer_message"
          disabled
        />
        <div><strong>回复消息：</strong></div>
        <el-input
          type="textarea"
          :rows="4"
          :model-value="viewDialog.data?.receiver_message"
          disabled
        />
      </div>
      <template #footer>
        <el-button @click="viewDialog.visible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="editDialog.visible"
      width="640px"
      :title="editDialog.isEdit ? '编辑消息' : '新增消息'"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="space-y-2">
        <el-form-item label="客户名称" prop="customer_name">
          <el-input v-model="form.customer_name" />
        </el-form-item>

        <el-form-item label="手机号" prop="customer_phone">
          <el-input v-model="form.customer_phone" />
        </el-form-item>

        <el-form-item label="客户消息" prop="customer_message">
          <el-input type="textarea" :rows="4" v-model="form.customer_message" />
        </el-form-item>

        <el-form-item label="回复消息" prop="receiver_message">
          <el-input type="textarea" :rows="4" v-model="form.receiver_message" />
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

// Element Plus 组件显式导入（严格按你要求）
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
  getCustomerMessageListApi,
  createCustomerMessageApi,
  updateCustomerMessageApi,
  deleteCustomerMessageApi,
} from '@/api/bot/customer/customer'

// 类型
interface MessageItem {
  id: number
  customer_phone?: string
  customer_name?: string
  customer_message?: string
  receiver_message?: string
}

// 分页对象（统一格式）
const paging = reactive({ page: 1, limit: 10, total: 0, v_order: 'desc' })

// 列表与筛选
const list = ref<MessageItem[]>([])
const filters = reactive({ keyword: '' })

// 获取列表
const fetchList = async () => {
  const params = {
    page: paging.page,
    limit: paging.limit,
    keyword: filters.keyword,
    v_order: paging.v_order,
  }
  try {
    const res: any = await getCustomerMessageListApi(params)
    if (res && res.data) {
      list.value = res.data || []
      paging.total = res.data.total ?? 0
    } else {
      list.value = []
      paging.total = 0
    }
  } catch (error) {
    console.error('fetchList error', error)
    ElMessage.error('获取消息列表失败')
  }
}

// 搜索
const onSearch = () => {
  paging.page = 1
  fetchList()
}

// 分页回调
const onPageChange = (page: number) => {
  paging.page = page
  fetchList()
}
const onLimitChange = (limit: number) => {
  paging.limit = limit
  paging.page = 1
  fetchList()
}

// 弹窗数据
const viewDialog = reactive({ visible: false, data: null as MessageItem | null })
const editDialog = reactive({ visible: false, isEdit: false, data_id: 0 })

// 表单
const formRef = ref()
const form = reactive({
  customer_name: '',
  customer_phone: '',
  customer_message: '',
  receiver_message: '',
})
const rules = reactive({
  customer_name: [{ required: true, message: '请输入客户名称', trigger: 'blur' }],
  customer_phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  customer_message: [{ required: true, message: '请输入客户消息', trigger: 'blur' }],
})

// 查看详情
const onView = (row: MessageItem) => {
  viewDialog.data = row
  viewDialog.visible = true
}

// 编辑
const onEdit = (row: MessageItem) => {
  editDialog.isEdit = true
  editDialog.data_id = row.id
  Object.assign(form, row)
  editDialog.visible = true
}

// 创建
const onOpenCreate = () => {
  editDialog.isEdit = false
  editDialog.data_id = 0
  Object.assign(form, {
    customer_name: '',
    customer_phone: '',
    customer_message: '',
    receiver_message: '',
  })
  editDialog.visible = true
}

const onCloseEdit = () => {
  editDialog.visible = false
}

// 提交创建/编辑
const onSubmitForm = () => {
  ;(formRef.value as any)?.validate?.(async (valid: boolean) => {
    if (!valid) return

    if (editDialog.isEdit && editDialog.data_id) {
      try {
        await updateCustomerMessageApi(editDialog.data_id, { ...form })
        ElMessage.success('更新成功')
        editDialog.visible = false
        fetchList()
      } catch (e) {
        ElMessage.error('更新失败')
      }
    } else {
      try {
        await createCustomerMessageApi({ ...form })
        ElMessage.success('创建成功')
        editDialog.visible = false
        fetchList()
      } catch (e) {
        ElMessage.error('创建失败')
      }
    }
  })
}

// 删除
const onDel = (row: MessageItem) => {
  ElMessageBox.confirm('确认删除该消息记录吗？', '删除确认', { type: 'warning' })
    .then(async () => {
      try {
        await deleteCustomerMessageApi([row.id])
        ElMessage.success('删除成功')
        fetchList()
      } catch (e) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {})
}

// 初始化加载
onMounted(() => {
  fetchList()
})
</script>

<style scoped>
/* tailwindcss 样式已足够，若需额外样式可添加 */
</style>
