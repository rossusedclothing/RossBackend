import request from '@/config/axios'

//表单列表
export const getBusinessFormLists = (params?: any) => {
    return request.get({ url: '/businessform/list/index', params })
}

export const deleteRecord = (ids: number[]) => {
    return request.delete({ url: '/businessform/list/delete', data: ids })
}
