import request from '@/config/axios'

//表单列表
export const getBusinessFormLists = (params?: any) => {
  return request.get({ url: '/businessform/bform/list', params })
}

export const deleteRecord = (ids: number[]) => {
  return request.delete({ url: '/businessform/bform/list', data: ids })
}

export const createBusinessForm = (data: any) => {
  return request.post({ url: '/businessform/bform/list', data })
}
