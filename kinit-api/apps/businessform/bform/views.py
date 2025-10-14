#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/13 12:18
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import crud, params, schemas

app = APIRouter()


###########################################################
#    客户表单
###########################################################

@app.get("/list", summary="获取客户表单列表", tags=["客户表单"])
async def get_business_form_list(
    p: params.BusinessFormParams = Depends(), 
    auth: Auth = Depends(AllUserAuth())
):
    """获取客户表单列表"""
    datas, count = await crud.BusinessFormDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)

'''#Ref：
# 在 FastAPI 后端，确保这个路由不需要认证
@router.post("/businessform/bform/list")
async def create_business_form(data: BusinessFormCreate):
    # 不需要 auth 依赖
    return await crud.BusinessFormDal(db).create_data(data=data)
'''
@app.post("/list", summary="创建客户表单", tags=["客户表单"])
async def create_business_form(
    data: schemas.BusinessFormCreate, 
    ###### auth: Auth = Depends(AllUserAuth())
):
    """创建客户表单"""
    return SuccessResponse(await crud.BusinessFormDal(db).create_data(data=data)) 


@app.delete("/list", summary="删除客户表单", description="删除", tags=["客户表单"])
async def delete_business_form_list(
    ids: IdList = Depends(), 
    auth: Auth = Depends(AllUserAuth())
):
    """批量删除客户表单"""
    await crud.BusinessFormDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/list/{data_id}", summary="更新客户表单", tags=["客户表单"])
async def put_business_form(
    data_id: int, 
    data: schemas.BusinessFormUpdate, 
    auth: Auth = Depends(AllUserAuth())
):
    """更新客户表单"""
    return SuccessResponse(await crud.BusinessFormDal(auth.db).put_data(data_id, data))


@app.get("/list/{data_id}", summary="获取客户表单信息", tags=["客户表单"])
async def get_business_form(
    data_id: int, 
    db: AsyncSession = Depends(db_getter)
):
    """根据ID获取客户表单详情"""
    schema = schemas.BusinessFormSimpleOut
    return SuccessResponse(await crud.BusinessFormDal(db).get_data(data_id, v_schema=schema))