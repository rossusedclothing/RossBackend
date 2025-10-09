<template>
  <el-input v-model="keyword" placeholder="搜索联系人" clearable class="mb-2" />
  <el-scrollbar height="calc(100vh - 50px)">
    <el-menu :default-active="String(activeId)" @select="onSelect" class="border-0">
      <el-menu-item v-for="c in filteredContacts" :key="c.id" :index="String(c.id)">
        <el-avatar :src="c.avatar" size="small" class="mr-2" />
        {{ c.name }}
      </el-menu-item>
    </el-menu>
  </el-scrollbar>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'

interface Contact {
  id: number
  name: string
  avatar: string
}

const props = defineProps<{
  contacts: Contact[]
}>()
const emit = defineEmits<{
  (e: 'select', contact: Contact): void
}>()

const keyword = ref('')
const activeId = ref<number | null>(null)

const filteredContacts = computed(() =>
  props.contacts.filter((c) => c.name.toLowerCase().includes(keyword.value.toLowerCase()))
)

function onSelect(id: string) {
  const contact = props.contacts.find((c) => c.id === Number(id))
  if (contact) {
    activeId.value = contact.id
    emit('select', contact)
  }
}
</script>
