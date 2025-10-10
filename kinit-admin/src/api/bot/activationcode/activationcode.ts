import request from '@/config/axios'

// 激活码相关
export const getActivationCodes = (params?: any) => {
  return request.get({ url: '/bot/activation/codes', params })
}

export const createActivationCode = (data: any) => {
  return request.post({ url: '/bot/activation/codes', data })
}

export const createGenerateCode = () => {
  return request.get({ url: `/bot/activation/generate/codes` })
}

export const updateActivationCode = (data_id: number, data: any) => {
  return request.put({ url: `/bot/activation/codes/${data_id}`, data })
}

export const deleteActivationCodes = (ids: number[]) => {
  return request.delete({ url: '/bot/activation/codes', data: ids })
}

// 生成激活码
export const generateActivationCodes = (params?: any) => {
  return request.get({ url: '/bot/activation/generate/codes', params })
}

// 使用记录相关
export const getActivationRecords = (params?: any) => {
  return request.get({ url: '/bot/activation/records', params })
}

export const createActivationRecord = (data: any) => {
  return request.post({ url: '/bot/activation/records', data })
}

export const updateActivationRecord = (data_id: number, data: any) => {
  return request.put({ url: `/bot/activation/records/${data_id}`, data })
}

export const deleteActivationRecords = (ids: number[]) => {
  return request.delete({ url: '/bot/activation/records', data: { ids } })
}
