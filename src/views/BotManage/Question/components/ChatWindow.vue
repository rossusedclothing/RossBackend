<template>
  <div class="flex flex-col h-full">
    <!-- 顶部联系人信息 -->
    <div class="flex items-center p-3 border-b">
      <el-avatar :src="contact.avatar" class="mr-2" />
      <span class="font-bold">{{ contact.name }}</span>
    </div>

    <!-- 消息区 -->
    <el-scrollbar class="flex-1 p-3">
      <div v-for="(m, i) in messages" :key="i" class="mb-2">
        <div
          :class="[
            'p-2 rounded max-w-xs',
            m.from === 'me' ? 'bg-green-100 self-end ml-auto' : 'bg-gray-100'
          ]"
        >
          {{ m.text }}
        </div>
      </div>
    </el-scrollbar>

    <!-- 输入框 -->
    <div class="p-3 border-t flex items-center">
      <el-input
        v-model="input"
        placeholder="输入消息..."
        class="flex-1 mr-2"
        @keyup.enter="sendMessage"
      />
      <el-button type="primary" @click="sendMessage">发送</el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Contact {
  id: number
  name: string
  avatar: string
}

interface Message {
  from: 'me' | 'other'
  text: string
}

const props = defineProps<{
  contact: Contact
}>()

const messages = ref<Message[]>([
  { from: 'other', text: 'Hi! 👋' },
  { from: 'me', text: 'Hello!' }
])

const input = ref('')

function sendMessage() {
  if (!input.value.trim()) return
  messages.value.push({ from: 'me', text: input.value })
  input.value = ''
}
</script>
