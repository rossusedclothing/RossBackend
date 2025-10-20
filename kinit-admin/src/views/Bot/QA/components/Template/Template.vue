<template>
  <div class="p-4 bg-white rounded-lg shadow">
    <!-- 搜索和操作区域 -->
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center space-x-2">
        <ElSelect
          v-model="searchParams.sale_agent_id"
          placeholder="业务员"
          clearable
          style="width: 120px"
          @change="handleSearch"
        >
          <ElOption
            v-for="item in saleAgentList"
            :key="item.value"
            :value="item.value"
            :label="item.label"
            >{{ item.label }}</ElOption
          >
        </ElSelect>
        <el-input
          v-model="searchParams.title"
          placeholder="搜索标题"
          clearable
          style="width: 200px"
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        />
        <el-select
          v-model="searchParams.status"
          placeholder="状态"
          clearable
          style="width: 120px"
          @change="handleSearch"
        >
          <el-option label="启用" :value="1" />
          <el-option label="禁用" :value="0" />
        </el-select>
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button @click="handleReset">
          <el-icon><Refresh /></el-icon>
          重置
        </el-button>
      </div>
      <el-button type="primary" @click="onAdd">
        <el-icon><Plus /></el-icon>
        新增模板
      </el-button>
    </div>

    <!-- 表格区域 -->
    <el-table :data="tableData" v-loading="loading" border stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" align="center" />
      <el-table-column prop="title" label="标题" min-width="150" show-overflow-tooltip />
      <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
      <el-table-column prop="status" label="状态" width="100" align="center">
        <template #default="scope">
          <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'" size="small">
            {{ scope.row.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="sale_agent_id" label="业务员" width="120" align="center">
        <template #default="scope">
          {{ selectDictLabel(saleAgentList, scope.row.sale_agent_id) }}
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="180" align="center">
        <template #default="scope">
          {{ formatTime(scope.row.create_time) }}
        </template>
      </el-table-column>
      <el-table-column prop="update_time" label="更新时间" width="180" align="center">
        <template #default="scope">
          {{ formatTime(scope.row.update_time) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="260" fixed="right">
        <template #default="scope">
          <el-button size="small" @click="onSetQA(scope.row)">设置</el-button>
          <el-button size="small" @click="onView(scope.row)">查看</el-button>
          <el-button size="small" type="primary" @click="onEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="onDel(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页区域 -->
    <div class="flex justify-end mt-4">
      <el-pagination
        v-model:current-page="paging.page"
        v-model:page-size="paging.limit"
        :page-sizes="[10, 20, 50, 100]"
        :total="paging.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="
        dialogType === 'add'
          ? '新增问题模板'
          : dialogType === 'edit'
            ? '编辑问题模板'
            : '查看问题模板'
      "
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        :disabled="dialogType === 'view'"
      >
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="formData.title"
            placeholder="请输入标题"
            maxlength="125"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入描述"
            maxlength="2048"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="售前代理ID" prop="sale_agent_id">
          <el-select
            v-model="formData.sale_agent_id"
            placeholder="请选择售前代理"
            clearable
            style="width: 100%"
          >
            <ElOption
              v-for="item in saleAgentList"
              :key="item.value"
              :value="item.value"
              :label="item.label"
              >{{ item.label }}</ElOption
            >
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button
            v-if="dialogType !== 'view'"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, reactive, ref } from 'vue'
// 导入所需的 Element Plus 组件
import {
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElIcon,
  ElInput,
  ElMessage,
  ElMessageBox,
  ElOption,
  ElPagination,
  ElRadio,
  ElRadioGroup,
  ElSelect,
  ElTable,
  ElTableColumn,
  ElTag,
  type FormInstance,
  type FormRules,
} from 'element-plus'
import { Plus, Refresh, Search } from '@element-plus/icons-vue'
import {
  createQuestionTemplateApi,
  deleteQuestionTemplateApi,
  getQuestionTemplateListApi,
  updateQuestionTemplateApi,
} from '@/api/bot/qa/questiong'
import { getUserListApi } from '@/api/vadmin/auth/user'
import { selectDictLabel } from '@/utils/dict'

const props = defineProps({
  tabParams: {
    type: Object,
    default: () => ({}),
  },
})
const emit = defineEmits(['switch-tab'])

// 类型定义
interface QuestionTemplate {
  id?: number
  title: string
  description: string
  status: number
  sale_agent_id: number
  create_time?: string
  update_time?: string
}

interface SearchParams {
  title?: string
  status?: number
}

interface Paging {
  page: number
  limit: number
  total: number
  v_order: 'desc' | 'asc'
  v_order_field?: string
}

// 响应式数据
const loading = ref(false)
const dialogVisible = ref(false)
const submitLoading = ref(false)
const dialogType = ref<'add' | 'edit' | 'view'>('add')
const formRef = ref<FormInstance>()
const tableData = ref<QuestionTemplate[]>([])

const searchParams = reactive<SearchParams>({
  title: '',
  status: undefined,
  sale_agent_id: undefined,
})

const paging = reactive<Paging>({
  page: 1,
  limit: 10,
  total: 0,
  v_order: 'desc',
})

const formData = reactive<QuestionTemplate>({
  title: '',
  description: '',
  status: 1,
  sale_agent_id: 0,
})

// 表单验证规则
const formRules: FormRules = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 1, max: 125, message: '标题长度在 1 到 125 个字符', trigger: 'blur' },
  ],
  description: [
    { required: true, message: '请输入描述', trigger: 'blur' },
    { min: 1, max: 2048, message: '描述长度在 1 到 2048 个字符', trigger: 'blur' },
  ],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
  sale_agent_id: [
    { required: true, message: '请输入售前代理ID', trigger: 'blur' },
    { type: 'number', min: 0, message: '售前代理ID不能为负数', trigger: 'blur' },
  ],
}

const saleAgentList = ref<any[]>([])

// 方法
const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString()
}

const handleSearch = () => {
  paging.page = 1
  getTableData()
}

const handleReset = () => {
  searchParams.title = ''
  searchParams.status = undefined
  paging.page = 1
  getTableData()
}

const handleSizeChange = (val: number) => {
  paging.limit = val
  paging.page = 1
  getTableData()
}

const handleCurrentChange = (val: number) => {
  paging.page = val
  getTableData()
}

const resetForm = () => {
  formData.title = ''
  formData.description = ''
  formData.status = 1
  formData.sale_agent_id = 0
  formRef.value?.clearValidate()
}

const onAdd = () => {
  dialogType.value = 'add'
  dialogVisible.value = true
  nextTick(() => {
    resetForm()
  })
}

const onEdit = async (row: QuestionTemplate) => {
  dialogType.value = 'edit'
  dialogVisible.value = true
  nextTick(() => {
    Object.assign(formData, row)
  })
}

const onSetQA = async (row: QuestionTemplate) => {
  emit('switch-tab', {
    tabName: 'QAndA',
    params: row,
  })
}

const onView = async (row: QuestionTemplate) => {
  dialogType.value = 'view'
  dialogVisible.value = true
  nextTick(() => {
    Object.assign(formData, row)
  })
}

const onDel = async (row: QuestionTemplate) => {
  try {
    await ElMessageBox.confirm(`确定要删除问题模板 "${row.title}" 吗？`, '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    await deleteQuestionTemplateApi([row.id])
    ElMessage.success('删除成功')
    getTableData()
  } catch (error) {
    // 用户取消删除
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  const valid = await formRef.value.validate()
  if (!valid) return

  submitLoading.value = true
  try {
    if (dialogType.value === 'add') {
      await createQuestionTemplateApi(formData)
      ElMessage.success('新增成功')
    } else if (dialogType.value === 'edit') {
      await updateQuestionTemplateApi(formData.id!, formData)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    getTableData()
  } catch (error) {
    // 错误处理已在请求拦截器中处理
  } finally {
    submitLoading.value = false
  }
}

const getTableData = async () => {
  loading.value = true
  try {
    const params = {
      ...searchParams,
      ...paging,
    }
    const res = await getQuestionTemplateListApi(params)
    tableData.value = res.data || []
    paging.total = res.data.total || 0
  } catch (error) {
    tableData.value = []
    paging.total = 0
  } finally {
    loading.value = false
  }
}
const getSaleAgentList = async () => {
  await getUserListApi().then((res) => {
    let userlist = res.data
    userlist = userlist.map((user) => {
      return {
        label: user.name || user.nickname,
        value: user.id || 1,
      }
    })
    saleAgentList.value = userlist
  })
}

// 生命周期
onMounted(() => {
  getTableData()
  getSaleAgentList()
})
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
}
</style>
