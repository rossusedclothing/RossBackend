<template>
  <div class="qrcode-page">
    <el-card class="qrcode-card">
      <template #header>
        <h2>表单分享二维码</h2>
      </template>

      <div class="qrcode-content">
        <div class="qrcode-image">
          <!-- 可以使用 qrcode.vue 或其他二维码库 -->
          <div ref="qrcodeRef" class="qrcode"></div>
        </div>

        <div class="qrcode-info">
          <h3>客户信息登记表</h3>
          <p>扫描二维码填写客户信息</p>
          <el-input v-model="formUrl" readonly size="large" class="url-input">
            <template #append>
              <el-button @click="copyUrl">复制链接</el-button>
            </template>
          </el-input>
          <el-button type="primary" @click="downloadQRCode" class="download-btn">
            下载二维码
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { ElMessage } from 'element-plus'
  import QRCode from 'qrcode'

  const qrcodeRef = ref<HTMLElement>()
  const formUrl = ref('')

  // 生成二维码
  onMounted(() => {
    formUrl.value = `${window.location.origin}/public/business-form`

    if (qrcodeRef.value) {
      QRCode.toCanvas(
              qrcodeRef.value,
              formUrl.value,
              {
                width: 200,
                margin: 2
              },
              (error) => {
                if (error) console.error('生成二维码失败:', error)
              }
      )
    }
  })

  // 复制链接
  const copyUrl = async () => {
    try {
      await navigator.clipboard.writeText(formUrl.value)
      ElMessage.success('链接已复制到剪贴板')
    } catch (err) {
      ElMessage.error('复制失败')
    }
  }

  // 下载二维码
  const downloadQRCode = () => {
    const canvas = qrcodeRef.value?.querySelector('canvas')
    if (canvas) {
      const link = document.createElement('a')
      link.download = '客户信息登记表二维码.png'
      link.href = canvas.toDataURL()
      link.click()
    }
  }
</script>

<style scoped>
  .qrcode-page {
    padding: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #f5f7fa;
  }

  .qrcode-card {
    max-width: 600px;
    width: 100%;
  }

  .qrcode-content {
    display: flex;
    align-items: center;
    gap: 40px;
    flex-wrap: wrap;
  }

  .qrcode-image {
    flex-shrink: 0;
  }

  .qrcode-info {
    flex: 1;
    min-width: 250px;
  }

  .qrcode-info h3 {
    margin-bottom: 8px;
    color: #303133;
  }

  .qrcode-info p {
    margin-bottom: 20px;
    color: #606266;
  }

  .url-input {
    margin-bottom: 20px;
  }

  .download-btn {
    width: 100%;
  }

  @media (max-width: 768px) {
    .qrcode-content {
      flex-direction: column;
      text-align: center;
    }
  }
</style>