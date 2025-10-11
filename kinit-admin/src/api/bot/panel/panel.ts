// src/api/panel.ts
import request from '@/config/axios'

// ============== ApiKeys ==============
export const getApiKeysListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/bot/panel/apiKeys', params })
}

export const addApiKeyApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/bot/panel/apiKeys', data })
}

export const updateApiKeyApi = (data_id: number | string, data: any): Promise<IResponse> => {
  return request.put({ url: `/bot/panel/apiKeys/${data_id}`, data })
}

export const delApiKeyApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/bot/panel/apiKeys', data })
}

export const getApiKeyDetailApi = (data_id: number | string): Promise<IResponse> => {
  return request.get({ url: `/bot/panel/apiKeys/${data_id}` })
}

// ============== appFeedback ==============
export const getFeedbackListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/bot/panel/appFeedback', params })
}

export const addFeedbackApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/bot/panel/appFeedback', data })
}

export const updateFeedbackApi = (data_id: number | string, data: any): Promise<IResponse> => {
  return request.put({ url: `/bot/panel/appFeedback/${data_id}`, data })
}

export const delFeedbackApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/bot/panel/appFeedback', data })
}

export const getFeedbackDetailApi = (data_id: number | string): Promise<IResponse> => {
  return request.get({ url: `/bot/panel/appFeedback/${data_id}` })
}

// ============== appUpdate ==============
export const getAppUpdateListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/bot/panel/appUpdate', params })
}

export const addAppUpdateApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/bot/panel/appUpdate', data })
}

export const updateAppUpdateApi = (data_id: number | string, data: any): Promise<IResponse> => {
  return request.put({ url: `/bot/panel/appUpdate/${data_id}`, data })
}

export const delAppUpdateApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/bot/panel/appUpdate', data })
}

export const getAppUpdateDetailApi = (data_id: number | string): Promise<IResponse> => {
  return request.get({ url: `/bot/panel/appUpdate/${data_id}` })
}
