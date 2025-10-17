<template>
  <div class="qrcode-page">
    <el-card class="qrcode-card">
      <template #header>
        <h2>表单分享二维码</h2>
      </template>

      <div class="qrcode-content">
        <div class="qrcode-image">
          <!-- 使用 canvas 元素来生成二维码 -->
          <canvas ref="qrcodeRef" class="qrcode-canvas"></canvas>
        </div>

        <div class="qrcode-info">
          <h3>客户信息登记表</h3>
          <p>扫描二维码填写客户信息</p>
          <el-input v-model="formUrl" readonly size="large" class="url-input">
            <template #append>
              <el-button @click="copyUrl">复制链接</el-button>
            </template>
          </el-input>

          <!-- 新增：二维码URL显示 -->
          <div class="qrcode-url-display">
            <h4>二维码链接：</h4>
            <p class="url-text">{{ formUrl }}</p>
          </div>

          <el-button type="primary" @click="downloadQRCode" class="download-btn">
            下载二维码
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted,  computed } from 'vue'
  import { ElMessage } from 'element-plus'
  import QRCode from 'qrcode'
  import { useAuthStoreWithOut } from '@/store/modules/auth'

  const qrcodeRef = ref<HTMLCanvasElement>()
  const formUrl = ref('')

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

  // 生成二维码
  onMounted(() => {
    //ref-o：formUrl.value = `${window.location.origin}/businessform/publicform2`
    formUrl.value=generateFormUrl()

    if (qrcodeRef.value) {
      QRCode.toCanvas(
              qrcodeRef.value,
              formUrl.value,
              {
                width: 200,
                margin: 2,
              },
              (error) => {
                if (error) {
                  console.error('生成二维码失败:', error)
                  ElMessage.error('生成二维码失败')
                } else {
                  console.log('二维码生成成功')
                }
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
      // 降级方案
      const textArea = document.createElement('textarea')
      textArea.value = formUrl.value
      document.body.appendChild(textArea)
      textArea.select()
      try {
        document.execCommand('copy')
        ElMessage.success('链接已复制到剪贴板')
      } catch (fallbackErr) {
        ElMessage.error('复制失败')
      }
      document.body.removeChild(textArea)
    }
  }

  // 下载二维码
  const downloadQRCode = () => {
    if (qrcodeRef.value) {
      const link = document.createElement('a')
      link.download = '客户信息登记表二维码.png'
      link.href = qrcodeRef.value.toDataURL('image/png')
      link.click()
    } else {
      ElMessage.error('二维码未生成')
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
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .qrcode-canvas {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px;
    background: white;
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

  /* 新增：二维码URL显示样式 */
  .qrcode-url-display {
    margin-bottom: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 4px;
    border-left: 4px solid #409eff;
  }

  .qrcode-url-display h4 {
    margin-bottom: 8px;
    color: #303133;
    font-size: 14px;
  }

  .url-text {
    word-break: break-all;
    color: #606266;
    font-size: 13px;
    line-height: 1.4;
    margin: 0;
  }

  .download-btn {
    width: 100%;
  }

  @media (max-width: 768px) {
    .qrcode-page {
      padding: 20px;
    }

    .qrcode-content {
      flex-direction: column;
      text-align: center;
      gap: 20px;
    }

    .qrcode-url-display {
      text-align: left;
    }
  }
</style>