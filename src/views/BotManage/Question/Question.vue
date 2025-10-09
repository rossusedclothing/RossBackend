<script setup lang="tsx">
import { ContentWrap } from '@/components/ContentWrap'
import { FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { useValidator } from '@/hooks/web/useValidator'
import { reactive } from 'vue'
const { required } = useValidator()

const formSchema = reactive<FormSchema[]>([
  {
    field: 'web_title',
    label: '系统标题',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  }
])

const rules = reactive({
  web_title: [required()],
  web_logo: [required()],
  web_ico: [required()]
})

const { formRegister, formMethods } = useForm()
</script>

<template>
  <ContentWrap>
    <Form :rules="rules" @register="formRegister" :schema="formSchema" />
  </ContentWrap>
</template>

<style scoped>
input {
  outline: none;
}
</style>
