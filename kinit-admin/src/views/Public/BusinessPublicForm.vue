<!-- src/views/public/business-form.vue -->
<template>

                        <div class="page-wrapper">
                            <div class="public-form-container">

    <div class="public-form-container">
        <!-- 页头 -->
        <div class="form-header">
            <div class="header-content">
                <h1 class="form-title">客户信息登记表</h1>
                <p class="form-description">欢迎填写客户信息，我们将尽快与您联系</p>
            </div>
        </div>

        <!-- 表单内容 -->
        <div class="form-content">
            <el-card class="form-card" shadow="hover">
                <el-form
                        ref="formRef"
                        :model="formData"
                        :rules="formRules"
                        label-width="120px"
                        label-position="left"
                >
                    <!-- 基本信息 -->
                    <el-divider content-position="left">
                        <span class="section-title">基本信息</span>
                    </el-divider>

                    <el-row :gutter="20">
                        <el-col :xs="24" :sm="12">
                            <el-form-item label="姓名" prop="name">
                                <el-input
                                        v-model="formData.name"
                                        placeholder="请输入您的姓名"
                                        maxlength="50"
                                        size="large"
                                />
                            </el-form-item>
                        </el-col>
                        <el-col :xs="24" :sm="12">
                            <el-form-item label="职位" prop="position">
                                <el-input
                                        v-model="formData.position"
                                        placeholder="请输入您的职位"
                                        maxlength="50"
                                        size="large"
                                />
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row :gutter="20">
                        <el-col :xs="24" :sm="12">
                            <el-form-item label="地区" prop="region">
                                <el-input
                                        v-model="formData.region"
                                        placeholder="请输入所在地区"
                                        maxlength="100"
                                        size="large"
                                />
                            </el-form-item>
                        </el-col>
                        <el-col :xs="24" :sm="12">
                            <el-form-item label="公司规模" prop="company_size">
                                <el-select
                                        v-model="formData.company_size"
                                        placeholder="请选择公司规模"
                                        size="large"
                                        style="width: 100%"
                                >
                                    <el-option label="1-10人" value="1-10人" />
                                    <el-option label="11-50人" value="11-50人" />
                                    <el-option label="51-200人" value="51-200人" />
                                    <el-option label="201-500人" value="201-500人" />
                                    <el-option label="500人以上" value="500人以上" />
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <!-- 业务信息 -->
                    <el-divider content-position="left">
                        <span class="section-title">业务信息</span>
                    </el-divider>

                    <el-form-item label="工厂规格" prop="factory_spec">
                        <el-input
                                v-model="formData.factory_spec"
                                placeholder="请描述工厂规模、设备等情况"
                                type="textarea"
                                :rows="3"
                                maxlength="200"
                                show-word-limit
                        />
                    </el-form-item>

                    <el-form-item label="主营产品" prop="product">
                        <el-input
                                v-model="formData.product"
                                placeholder="请输入公司主营产品"
                                maxlength="100"
                                size="large"
                        />
                    </el-form-item>

                    <el-form-item label="网站链接">
                        <el-input
                                v-model="formData.website"
                                placeholder="请输入公司官网或产品链接（可选）"
                                maxlength="200"
                                size="large"
                        />
                    </el-form-item>

                    <!-- 外贸信息 -->
                    <el-divider content-position="left">
                        <span class="section-title">外贸信息</span>
                    </el-divider>

                    <el-row :gutter="20">
                        <el-col :xs="24" :sm="12">
                            <el-form-item label="外贸经验" prop="has_export_experience">
                                <el-radio-group v-model="formData.has_export_experience" size="large">
                                    <el-radio :label="true">有外贸经验</el-radio>
                                    <el-radio :label="false">无外贸经验</el-radio>
                                </el-radio-group>
                            </el-form-item>
                        </el-col>
                        <el-col :xs="24" :sm="12">
                            <el-form-item label="外贸团队人数" prop="num_members_tradeteam">
                                <el-input-number
                                        v-model="formData.num_members_tradeteam"
                                        :min="0"
                                        :max="1000"
                                        placeholder="0"
                                        size="large"
                                        controls-position="right"
                                        style="width: 100%"
                                />
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-form-item label="产品出口市场" prop="export_market">
                        <el-input
                                v-model="formData.export_market"
                                placeholder="请输入产品主要出口的国家或地区"
                                type="textarea"
                                :rows="3"
                                maxlength="200"
                                show-word-limit
                        />
                    </el-form-item>

                    <!-- 学员信息 -->
                    <el-divider content-position="left">
                        <span class="section-title">学员信息</span>
                    </el-divider>

                    <el-form-item label="学员身份" prop="student_identity">
                        <el-select
                                v-model="formData.student_identity"
                                placeholder="请选择学员身份"
                                size="large"
                                style="width: 100%"
                        >
                            <el-option label="新学员" value="新学员" />
                            <el-option label="在读学员" value="在读学员" />
                            <el-option label="毕业学员" value="毕业学员" />
                            <el-option label="意向学员" value="意向学员" />
                            <el-option label="其他" value="其他" />
                        </el-select>
                    </el-form-item>
                </el-form>

                <!-- 提交按钮 -->
                <div class="submit-section">
                    <el-button
                            type="primary"
                            @click="submitForm"
                            :loading="loading"
                            size="large"
                            class="submit-btn"
                    >
                        {{ loading ? '提交中...' : '立即提交' }}
                    </el-button>
                    <el-button @click="resetForm" :disabled="loading" size="large" class="reset-btn">
                        重新填写
                    </el-button>
                </div>
            </el-card>
        </div>

        <!-- 页脚 -->
        <!--#o：不带二维码版本
        <div class="form-footer">
          <p>如有问题，请联系我们：400-xxx-xxxx</p>
        </div>
        -->
        <!-- 修改页脚部分 -->
        <div class="form-footer">
            <div class="footer-content">
                <p>
                    如有问题，请点击联系我们：<a
                        href="mailto:2457676371@qq.com?subject=问题反馈&body=您好，我遇到的问题是："
                        style="color: #1890ff; text-decoration: underline; cursor: pointer"
                >发邮件</a
                >
                </p>
                <div class="footer-links"  style="display:none;">
                    <el-button link type="primary" @click="goToQRCodePage" class="qrcode-link">
                        <el-icon><Share /></el-icon>
                        生成分享二维码
                    </el-button>
                    <el-divider direction="vertical" />
                    <el-button link type="info" @click="copyFormLink">
                        <el-icon><Link /></el-icon>
                        复制表单链接
                    </el-button>
                </div>
            </div>
        </div>

        <!-- 浮动分享按钮 -->
        <div class="floating-share-btn" @click="showShareMenu = !showShareMenu"  style="display:none;">
            <el-icon size="20"><Share /></el-icon>
            <div v-if="showShareMenu" class="share-menu">
                <div class="share-item" @click.stop="goToQRCodePage"  style="color:black;">
                    <el-icon><Picture /></el-icon>
                    生成二维码
                </div>
                <div class="share-item" @click.stop="copyFormLink"  style="color:black;">
                    <el-icon><Link /></el-icon>
                    复制链接
                </div>
            </div>
        </div>

        <!-- 成功弹窗 -->
        <el-dialog
                v-model="successDialogVisible"
                title="提交成功"
                width="400px"
                :show-close="false"
                :close-on-click-modal="false"
                :close-on-press-escape="false"
        >
            <div class="success-content">
                <el-icon color="#67C23A" size="48">
                    <CircleCheck />
                </el-icon>
                <p class="success-message">感谢您的提交！我们会在24小时内与您联系。</p>
            </div>
            <template #footer>
                <el-button type="primary" @click="handleSuccessConfirm" size="large">
                    继续填写新表单
                </el-button>
            </template>
        </el-dialog>
    </div>
                            </div>
                        </div>
</template>


<script setup lang="ts">
    import {computed, onMounted, reactive, ref } from 'vue'
    import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
    import { CircleCheck, Link, Picture, Share } from '@element-plus/icons-vue'
    import { createBusinessForm } from '@/api/businessform/list/list'

    import { useAuthStoreWithOut } from '@/store/modules/auth'

    import { useRouter } from 'vue-router'

    const router = useRouter()

    const showShareMenu = ref(false) //?

    // 表单引用
    const formRef = ref<FormInstance>()

    // 状态管理
    const loading = ref(false)
    const successDialogVisible = ref(false)


    const authStore = useAuthStoreWithOut()
    const currentUser = computed(() => {
        //b：return authStore.getUserInfo
        return authStore.user // 直接访问 user 属性
    })
    const generateFormUrl = () => {
        const baseUrl = `${window.location.origin}/businessform/publicform2`
        /*
        Object.keys(currentUser).forEach(key => {
          alert(`字段: ${key}, 值:`, currentUser[key])
        })
        */


        if (currentUser.value?.id) {
            return `${baseUrl}?bt=${currentUser.value.id}`
        } else {
            return baseUrl
        }
    }

    const getBtParam = () => {
        const urlParams = new URLSearchParams(window.location.search)
        const btValue = urlParams.get('bt')
        return btValue
    }
    // 验证bt参数是否为有效的整型数值
    const validateBtParam = (btValue: string | null): boolean => {
        if (!btValue) {
            return false
        }

        // 检查是否为整型数值
        const num = Number(btValue)
        if (isNaN(num) || !Number.isInteger(num) || num <= 0) {
            return false
        }

        return true
    }

    // 表单数据
    const formData = reactive({
        name: '',
        position: '',
        region: '',
        factory_spec: '',
        product: '',
        website: '',
        has_export_experience: false,
        export_market: '',
        student_identity: '',
        num_members_tradeteam: 0,
        company_size: '',
        bt: '' // 添加 bt 字段
    })

    // 表单验证规则
    const formRules: FormRules = {
        name: [
            { required: true, message: '请输入姓名', trigger: 'blur' },
            { min: 2, max: 50, message: '姓名长度在 2 到 50 个字符', trigger: 'blur' },
        ],
        position: [
            { required: false, message: '请输入职位', trigger: 'blur' },
            { max: 50, message: '职位长度不能超过 50 个字符', trigger: 'blur' },
        ],
        region: [
            { required: true, message: '请输入地区', trigger: 'blur' },
            { max: 100, message: '地区长度不能超过 100 个字符', trigger: 'blur' },
        ],
        factory_spec: [
            { required: false, message: '请输入工厂规格', trigger: 'blur' },
            { max: 200, message: '工厂规格长度不能超过 200 个字符', trigger: 'blur' },
        ],
        product: [
            { required: true, message: '请输入主营产品', trigger: 'blur' },
            { max: 100, message: '产品名称长度不能超过 100 个字符', trigger: 'blur' },
        ],
        website: [
            { required: false, message: '请输入网站链接', trigger: 'blur' },
            { max: 200, message: '网站链接长度不能超过 200 个字符', trigger: 'blur' },
        ],
        export_market: [
            { required: false, message: '请输入出口市场', trigger: 'blur' },
            { max: 200, message: '出口市场描述长度不能超过 200 个字符', trigger: 'blur' },
        ],
        student_identity: [{ required: false, message: '请选择学员身份', trigger: 'change' }],
        company_size: [{ required: false, message: '请选择公司规模', trigger: 'change' }],
    }

    // 页面加载时设置标题
    onMounted(() => {
        document.title = '客户信息登记表'

        // 获取并验证bt参数
        const btValue = getBtParam()
        if (btValue) {
            if (validateBtParam(btValue)) {
                formData.bt = btValue
                console.log('有效的bt参数:', btValue)
            } else {
                ElMessage.error('分享链接参数错误，请联系分享人获取正确的链接')
                console.error('无效的bt参数:', btValue)
            }
        } else {
            console.log('未找到bt参数')
        }
    })

    // 提交表单
    const submitForm = async () => {
        if (!formRef.value) return

        try {
            const valid = await formRef.value.validate()
            if (!valid) return

            // 检查bt参数（如果存在）
            if (formData.bt && !validateBtParam(formData.bt)) {
                ElMessage.error('分享链接参数错误，请联系分享人获取正确的链接')
                return
            }

            loading.value = true

            //ref-o：const response = await createBusinessForm(formData)
            // 准备提交数据，包含bt参数
            const submitData = {
                ...formData,
                // 确保bt参数正确传递
                bt: formData.bt || null
            }
            const response = await createBusinessForm(submitData)


            if (response.code === 200) {
                successDialogVisible.value = true
            } else {
                ElMessage.error(response.message || '提交失败，请重试')
            }
        } catch (error: any) {
            console.error('提交失败:', error)
            if (error.response?.data?.detail) {
                ElMessage.error(`提交失败: ${error.response.data.detail}`)
            } else {
                ElMessage.error('网络错误，请检查网络连接后重试')
            }
        } finally {
            loading.value = false
        }
    }

    // 重置表单
    const resetForm = () => {
        ElMessageBox.confirm('确定要清空所有已填写的内容吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }).then(() => {
            // 保存当前的bt值
            const currentBt = formData.bt

            formRef.value?.resetFields()
            formData.num_members_tradeteam = 0
            formData.has_export_experience = false
            ElMessage.success('表单已重置')

            // 恢复bt值
            formData.bt = currentBt

        })
    }

    // 成功确认
    const handleSuccessConfirm = () => {
        successDialogVisible.value = false
        resetForm()
        // 滚动到顶部
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    // 跳转到二维码页面
    const goToQRCodePage = () => {
        router.push('/businessform/qrcode')
        // 使用 name 方式跳转更可靠
        //////router.push({ name: 'QRCode' })
    }

    // 复制表单链接
    const copyFormLink = async () => {
        //o-2-b：const formUrl = `${window.location.origin}/public/business-form`
        //ref-o：const formUrl = `${window.location.origin}/businessform/publicform2`
        let formUrl = generateFormUrl()

        try {
            await navigator.clipboard.writeText(formUrl)
            ElMessage.success('表单链接已复制到剪贴板')
        } catch (err) {
            ElMessage.error('复制失败，请手动复制链接')
        }
    }
</script>


<style>
    /* 全局样式修复 */
    html, body {
        height: auto !important;
        min-height: 100vh;
        overflow-y: auto !important;
    }

    #app {
        min-height: 100vh;
        height: auto !important;
    }
</style>

<style scoped>
    .page-wrapper {
        min-height: 100vh;
        overflow-y: auto;
    }

    .public-form-container {
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        /* 确保没有以下属性 */
        /* height: 100vh; */
        /* overflow: hidden; */
        /* position: fixed; */
    }

    .public-form-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        overflow-y: auto;  /* 添加这个允许垂直滚动 */
    }

    .form-header {
        text-align: center;
        color: white;
        margin-bottom: 30px;
        padding: 40px 20px 20px;
    }

    .header-content {
        max-width: 800px;
        margin: 0 auto;
    }

    .form-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 16px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .form-description {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }

    .form-content {
        max-width: 800px;
        margin: 0 auto 40px;
    }

    .form-card {
        border-radius: 16px;
        border: none;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.95);
    }

    :deep(.el-card__body) {
        padding: 40px;
    }

    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #409eff;
    }

    :deep(.el-divider__text) {
        background: transparent;
        padding: 0 20px;
    }

    .submit-section {
        text-align: center;
        margin-top: 40px;
        padding-top: 30px;
        border-top: 1px solid #e4e7ed;
    }

    .submit-btn {
        width: 200px;
        height: 50px;
        font-size: 16px;
        margin-right: 20px;
    }

    .reset-btn {
        width: 120px;
        height: 50px;
        font-size: 16px;
    }

    .form-footer {
        text-align: center;
        color: white;
        padding: 20px;
        opacity: 0.8;
    }

    .success-content {
        text-align: center;
        padding: 20px 0;
    }

    .success-message {
        margin-top: 16px;
        font-size: 16px;
        color: #606266;
        line-height: 1.6;
    }

    /* 原有的样式不变，添加以下样式 */

    .footer-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
    }

    .footer-links {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .qrcode-link {
        font-weight: 500;
    }

    .floating-share-btn {
        position: fixed;
        right: 30px;
        bottom: 30px;
        width: 60px;
        height: 60px;
        background: #409eff;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
        transition: all 0.3s ease;
        z-index: 1000;
    }

    .floating-share-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(64, 158, 255, 0.6);
    }

    .share-menu {
        position: absolute;
        bottom: 70px;
        right: 0;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        padding: 8px 0;
        min-width: 140px;
    }

    .share-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .share-item:hover {
        background: #f5f7fa;
    }

    .share-item .el-icon {
        color: #409eff;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .public-form-container {
            padding: 10px;
            overflow-y: auto;  /* 添加这个允许垂直滚动 */
        }

        .form-title {
            font-size: 2rem;
        }

        .form-description {
            font-size: 1rem;
        }

        :deep(.el-card__body) {
            padding: 20px;
        }

        :deep(.el-form-item__label) {
            padding-bottom: 8px;
        }

        .submit-btn,
        .reset-btn {
            width: 100%;
            margin: 5px 0;
        }

        .footer-links {
            flex-direction: column;
            gap: 16px;
        }

        .el-divider--vertical {
            /*暂时未用到吧~~？*/
            display: none;
        }
    }
</style>
