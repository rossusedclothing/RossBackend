// src/api/customer.ts
import request from '@/config/axios'

// 客户表
export const getCustomerListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/customer/customer', params })
}

export const createCustomerApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/customer/customer', data })
}

export const updateCustomerApi = (data_id: number, data: any): Promise<IResponse> => {
  return request.put({ url: `/customer/customer/${data_id}`, data })
}

export const deleteCustomerApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/customer/customer', data })
}

export const getCustomerInfoApi = (data_id: number): Promise<IResponse> => {
  return request.get({ url: `/customer/customer/${data_id}` })
}

// 历史消息表
export const getCustomerMessageListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/customer/message', params })
}

export const createCustomerMessageApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/customer/message', data })
}

export const updateCustomerMessageApi = (data_id: number, data: any): Promise<IResponse> => {
  return request.put({ url: `/customer/message/${data_id}`, data })
}

export const deleteCustomerMessageApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/customer/message', data })
}

// 业务员配置 & 工作流程（示例）
export const getSalesAgentConfigListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/customer/sales/agent/config', params })
}
export const createSalesAgentConfigApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/customer/sales/agent/config', data })
}
export const deleteSalesAgentConfigApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/customer/sales/agent/config', data })
}
export const updateSalesAgentConfigApi = (data_id: number, data: any): Promise<IResponse> => {
  return request.put({ url: `customer/sales/agent/config/${data_id}`, data })
}

export const getSalesAgentConfigInfoApi = (data_id: any): Promise<IResponse> => {
  return request.get({ url: `/customer/sales/agent/config/${data_id}` })
}

export const getSalesAgentWorkflowListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/customer/sales/agent/workflow', params })
}
export const createSalesAgentWorkflowApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/customer/sales/agent/workflow', data })
}
export const deleteSalesAgentWorkflowApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/customer/sales/agent/workflow', data })
}
export const updateSalesAgentWorkflowApi = (data_id, data: any): Promise<IResponse> => {
  return request.put({ url: `/customer/sales/agent/workflow/${data_id}`, data })
}

export const getSalesAgentWorkflowInfoApi = (data_id: any): Promise<IResponse> => {
  return request.get({ url: `/customer/sales/agent/workflow/${data_id}` })
}
