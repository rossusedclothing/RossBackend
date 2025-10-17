import request from '@/config/axios'

// 表单列表
export const getBusinessFormLists = (params?: any) => {
  return request.get({ url: '/businessform/bform/list', params })
}

// 获取单条表单记录
export const getBusinessForm = (id: number) => {
  return request.get({ url: `/businessform/bform/list/${id}` })
}

// 删除表单记录
export const deleteRecord = (ids: number[]) => {
  return request.delete({ url: '/businessform/bform/list', data: ids })
}

// 创建表单记录
export const createBusinessForm = (data: any) => {
  return request.post({ url: '/businessform/bform/list', data })
}

// 更新表单记录
export const updateBusinessForm = (id: number, data: any) => {
  return request.put({ url: `/businessform/bform/list/${id}`, data })
}

// 类型定义（可选，推荐添加）
export interface BusinessFormData {
  name: string
  position?: string
  region: string
  factory_spec?: string
  product: string
  website?: string
  has_export_experience: boolean
  export_market?: string
  student_identity?: string
  num_members_tradeteam: number
  company_size?: string
  bt?: number
}

export interface BusinessFormQueryParams {
  skip?: number
  limit?: number
  name?: string
  position?: string
  region?: string
  product?: string
  has_export_experience?: boolean
  student_identity?: string
  company_size?: string
  bt?: number
}