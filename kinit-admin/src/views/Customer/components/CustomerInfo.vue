<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-2">
        <el-input
          v-model="filters.keyword"
          placeholder="搜索手机号或姓名"
          clearable
          @clear="onSearch"
          @keydown.enter="onSearch"
        />
        <el-button :plain="true" @click="onSearch">搜索</el-button>
        <el-button type="primary" @click="onOpenCreate">创建客户</el-button>
      </div>

      <div class="text-sm text-gray-500"> 总数：{{ paging.total }} </div>
    </div>

    <el-table :data="list" stripe style="width: 100%" :empty-text="'暂无数据'">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="customer_name" label="客户名称" />
      <el-table-column prop="customer_phone" label="手机号" />
      <el-table-column prop="platform" label="平台" width="120" />
      <el-table-column prop="meta_data" label="元数据" show-overflow-tooltip />
      <!-- 操作列（严格按需求模版） -->
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
      width="600px"
      :title="'客户详情 - ' + (viewDialog.data?.customer_name || '')"
    >
      <div class="space-y-2">
        <div><strong>手机号：</strong>{{ viewDialog.data?.customer_phone }}</div>
        <div><strong>名称：</strong>{{ viewDialog.data?.customer_name }}</div>
        <div><strong>平台：</strong>{{ viewDialog.data?.platform }}</div>
        <div><strong>元数据：</strong></div>
        <el-input type="textarea" :rows="6" :model-value="viewDialog.data?.meta_data" disabled />
      </div>
      <template #footer>
        <el-button @click="viewDialog.visible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="editDialog.visible"
      width="640px"
      :title="editDialog.isEdit ? '编辑客户' : '创建客户'"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="space-y-2">
        <el-form-item label="客户名称" prop="customer_name">
          <el-input v-model="form.customer_name" />
        </el-form-item>

        <el-form-item label="手机号" prop="customer_phone">
          <el-input v-model="form.customer_phone" />
        </el-form-item>

        <el-form-item label="平台" prop="platform">
          <el-input v-model="form.platform" />
        </el-form-item>

        <el-form-item label="元数据" prop="meta_data">
          <el-input type="textarea" :rows="4" v-model="form.meta_data" />
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

// Element Plus 组件要逐个导入（按你要求）
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
  ElMessage
} from 'element-plus'

// API
import {
  getCustomerListApi,
  createCustomerApi,
  updateCustomerApi,
  deleteCustomerApi,
  getCustomerInfoApi
} from '@/api/bot/customer/customer'

// types (可根据项目补充)
interface CustomerItem {
  id: number
  sales_agent_id?: number
  customer_phone?: string
  customer_name?: string
  platform?: string
  meta_data?: string
}

// 分页对象（按要求）
const paging = reactive({ page: 1, limit: 10, total: 0, v_order: 'desc' })

// 列表 & 筛选
const list = ref<CustomerItem[]>([])
const filters = reactive({ keyword: '' })

// 获取列表
const fetchList = async () => {
  const params = {
    page: paging.page,
    limit: paging.limit,
    keyword: filters.keyword,
    v_order: paging.v_order
  }
  try {
    const res: any = await getCustomerListApi(params)
    // 假设后端返回结构 { code: 0, data: { list: [], total: 0 } }
    if (res && res.data) {
      list.value = res.data || []
      paging.total = res.data.total ?? 0
    } else {
      list.value = []
      paging.total = 0
    }
  } catch (error) {
    console.error('fetchList error', error)
    ElMessage.error('获取客户列表失败')
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

// 查看/编辑/删除 - 需与模板方法名一致
const viewDialog = reactive({ visible: false, data: null as CustomerItem | null })
const editDialog = reactive({ visible: false, isEdit: false, data_id: 0 })
const formRef = ref()
const form = reactive({
  customer_name: '',
  customer_phone: '',
  platform: 'whatsapp',
  meta_data: ''
})
const rules = reactive({
  customer_name: [{ required: true, message: '请输入客户名称', trigger: 'blur' }],
  customer_phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }]
})

const onView = (row: CustomerItem) => {
  // 可选：拉取详情
  if (row?.id) {
    getCustomerInfoApi(row.id)
      .then((res: any) => {
        if (res && res.data) {
          viewDialog.data = res.data
        } else {
          viewDialog.data = row
        }
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

const onEdit = (row: CustomerItem) => {
  editDialog.isEdit = true
  editDialog.data_id = row.id
  form.customer_name = row.customer_name || ''
  form.customer_phone = row.customer_phone || ''
  form.platform = row.platform || 'whatsapp'
  form.meta_data = row.meta_data || ''
  editDialog.visible = true
}

const onOpenCreate = () => {
  editDialog.isEdit = false
  editDialog.data_id = 0
  form.customer_name = ''
  form.customer_phone = ''
  form.platform = 'whatsapp'
  form.meta_data = ''
  editDialog.visible = true
}

const onCloseEdit = () => {
  editDialog.visible = false
}

// 提交创建/编辑
const onSubmitForm = () => {
  // 表单验证
  ;(formRef.value as any)?.validate?.(async (valid: boolean) => {
    if (!valid) return
    if (editDialog.isEdit && editDialog.data_id) {
      try {
        await updateCustomerApi(editDialog.data_id, { ...form })
        ElMessage.success('更新成功')
        editDialog.visible = false
        fetchList()
      } catch (e) {
        ElMessage.error('更新失败')
      }
    } else {
      try {
        await createCustomerApi({ ...form })
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
const onDel = (row: CustomerItem) => {
  ElMessageBox.confirm('确认删除该客户吗？', '删除确认', { type: 'warning' })
    .then(async () => {
      try {
        // 后端 delete 示例通常支持批量删除，这里按你的封装示例传 data
        await deleteCustomerApi([row.id])
        ElMessage.success('删除成功')
        fetchList()
      } catch (e) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {
      // 取消
    })
}

// 初始化
onMounted(() => {
  fetchList()
})
</script>

<style scoped>
/* 你可以在这里继续写 tailwind + 自定义 css */
</style>
