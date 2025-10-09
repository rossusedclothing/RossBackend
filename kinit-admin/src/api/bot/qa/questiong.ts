import request from '@/config/axios'

export const getQuestionListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/bot/qa/question', params })
}

export const delQuestionApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/bot/qa/question', data })
}

export const addQuestionListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/bot/qa/question', data })
}

export const putQuestionListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/bot/qa/question/${data.id}`, data })
}

export const getQuestionTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/bot/qa/question/tree/options' })
}

export const getQuestionUserTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/bot/qa/dept/user/tree/options' })
}

export const getAnswerListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/bot/qa/answer', params })
}

export const addAnswerListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/bot/qa/answer', data })
}

export const putAnswerListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/bot/qa/answer/${data.id}`, data })
}

export const delAnswerListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/bot/qa/answer', data })
}
