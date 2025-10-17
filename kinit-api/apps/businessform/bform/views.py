#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/13 12:18
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件

#r-2-b：from core.db import get_db  # 导入获取数据库会话的函数
from core.database import db_getter
from fastapi import Depends, APIRouter,  HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import crud, params, schemas

from sqlalchemy.ext.asyncio import AsyncSession  # 若已有此导入，可直接在后面加
from sqlalchemy.exc import SQLAlchemyError  # 新增这行，导入SQLAlchemy异常基类
##from core.db import get_db  # 假设你有数据库会话的依赖

from typing import Optional  # 确保有 Optional 导入



app = APIRouter()


###########################################################
#    客户表单
###########################################################

@app.get("/list", summary="获取客户表单列表", tags=["客户表单"])
async def get_business_form_list(
    p: params.BusinessFormParams = Depends(),
    bt: Optional[int] = Query(None, description="按分享人用户ID筛选"),  # 新增 bt 查询参数
    auth: Auth = Depends(AllUserAuth())
):
    """获取客户表单列表"""
    '''#o：
    datas, count = await crud.BusinessFormDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)
    '''
    """获取客户表单列表"""
    # 构建查询参数
    query_params = p.dict()

    # 如果提供了 bt 参数，添加到查询参数中
    if bt is not None:
        query_params['bt'] = bt

    datas, count = await crud.BusinessFormDal(auth.db).get_datas(**query_params, v_return_count=True)
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
    # 1. 通过 Depends(get_db) 获取数据库会话（关键：确保 db 被定义）
    #r-2-b：db: AsyncSession = Depends(get_db)
    db: AsyncSession = Depends(db_getter)
):
    try:
        # 2. 调用 BusinessFormDal 时传入 db 参数（关键：传递 db）
        dal = crud.BusinessFormDal(db)
        result = await dal.create_data(data=data)
        #o-2-b：return SuccessResponse(result)
        # 直接返回字典（FastAPI 能自动序列化为 JSON）
        return SuccessResponse(data=result)  # 若 SuccessResponse 需模型实例，可改为直接返回 dict
    except SQLAlchemyError as e:
        ###await db.rollback()
        raise HTTPException(status_code=500, detail=f"数据库错误：{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"接口错误：{str(e)}")


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