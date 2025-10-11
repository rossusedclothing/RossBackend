<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <el-input
          v-model="filters.platform"
          placeholder="平台名称 / key / app 名称"
          clearable
          @clear="onSearch"
          @keyup.enter="onSearch"
        />
        <el-button @click="onSearch" type="primary" plain>搜索</el-button>
      </div>
      <div>
        <el-button @click="openCreate" type="primary">新建 ApiKey</el-button>
      </div>
    </div>

    <el-table :data="list" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="platform" label="平台" />
      <el-table-column prop="key_value" label="Key" />
      <el-table-column prop="useapp_name" label="所属 App" />
      <el-table-column prop="desc" label="描述" />
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
        :current-page="paging.page"
        :page-size="paging.pageSize"
        :total="paging.total"
        layout="prev, pager, next, jumper, ->, total"
        @current-change="onPageChange"
      />
    </div>

    <!-- create / edit dialog -->
    <el-dialog :title="dialogTitle" v-model="showDialog" width="520px">
      <el-form :model="form" ref="formRef" label-width="100px">
        <el-form-item
          label="平台"
          prop="platform"
          :rules="[{ required: true, message: '请输入平台', trigger: 'blur' }]"
        >
          <el-select v-model="form.platform" placeholder="选择平台">
            <el-option
              v-for="(item, index) in platformList"
              :key="index"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item
          label="Key"
          prop="key_value"
          :rules="[{ required: true, message: '请输入 key', trigger: 'blur' }]"
        >
          <el-input v-model="form.key_value" />
        </el-form-item>

        <el-form-item label="App 名称" prop="useapp_name">
          <el-input v-model="form.useapp_name" />
        </el-form-item>

        <el-form-item label="描述" prop="desc">
          <el-input v-model="form.desc" />
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
  ElSelect,
  ElOption
} from 'element-plus'
import {
  getApiKeysListApi,
  addApiKeyApi,
  updateApiKeyApi,
  delApiKeyApi,
  getApiKeyDetailApi
} from '@/api/bot/panel/panel'

const list = ref<any[]>([])
const paging = reactive({ page: 1, pageSize: 10, total: 0 })
const filters = reactive({ platform: '' })

const showDialog = ref(false)
const dialogTitle = ref('新建 ApiKey')
const isEdit = ref(false)
const editId = ref<number | null>(null)
const form = reactive({
  platform: '',
  key_value: '',
  useapp_name: '',
  desc: ''
})

const platformList = reactive([
  { label: 'openai', value: 'openai' },
  { label: 'deepseek', value: 'deepseek' },
  { label: '智普清言', value: '智普清言' },
  { label: 'siliconflow', value: 'siliconflow' },
  { label: 'google', value: 'google' },
  { label: 'tongyi', value: 'tongyi' },
  { label: 'coze', value: 'coze' },
  { label: 'huosan', value: 'huosan' },
  { label: 'other', value: 'other' }
])

const formRef = ref()

const load = async () => {
  const params = { page: paging.page, pageSize: paging.pageSize, ...filters }
  const res: any = await getApiKeysListApi(params)
  // 假设返回结构为 { data: { list: [], total: n } }
  if (res && res.data) {
    console.log(res.data)
    list.value = res.data || []
    paging.total = res.data.total || list.value.length
  }
  console.log('list', list.value)
}

onMounted(load)

const onSearch = () => {
  paging.page = 1
  load()
}

const onPageChange = (page: number) => {
  paging.page = page
  load()
}

const openCreate = () => {
  isEdit.value = false
  editId.value = null
  dialogTitle.value = '新建 ApiKey'
  Object.assign(form, { platform: '', key_value: '', useapp_name: '', desc: '' })
  showDialog.value = true
}

const onEdit = async (row: any) => {
  isEdit.value = true
  editId.value = row.id
  dialogTitle.value = '编辑 ApiKey'
  const res: any = await getApiKeyDetailApi(row.id)
  if (res && res.data) {
    Object.assign(form, res.data)
  } else {
    Object.assign(form, {
      platform: row.platform,
      key_value: row.key_value,
      useapp_name: row.useapp_name,
      desc: row.desc
    })
  }
  showDialog.value = true
}

const onView = async (row: any) => {
  const res: any = await getApiKeyDetailApi(row.id)
  ElMessageBox.alert(JSON.stringify(res.data || row, null, 2), 'ApiKey 详情', {
    dangerouslyUseHTMLString: false
  })
}

const onSubmit = async () => {
  try {
    await (isEdit.value ? updateApiKeyApi(editId.value as number, form) : addApiKeyApi(form))
    ElMessage({ message: '保存成功', type: 'success' })
    showDialog.value = false
    load()
  } catch (e) {
    ElMessage({ message: '保存失败', type: 'error' })
  }
}

const onDel = (row: any) => {
  ElMessageBox.confirm(`确认删除 ID=${row.id} ?`, '删除确认', { type: 'warning' })
    .then(async () => {
      // 后端 delete 接口设计是接受 { ids: [..] } 或一条数据，根据你的实现调整
      await delApiKeyApi([row.id])
      ElMessage({ message: '删除成功', type: 'success' })
      load()
    })
    .catch(() => {})
}
</script>

<style scoped>
/* 你可以在这里加更多 Tailwind 或自定义样式 */
</style>
