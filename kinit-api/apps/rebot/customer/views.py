#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/15 11:36
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
from fastapi import Depends, APIRouter, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter
from core.dependencies import IdList
from utils.response import SuccessResponse, ErrorResponse
from . import params, crud, schemas

app = APIRouter()


###########################################################
#    客户表
###########################################################
@app.get("/customer", summary="获取客户表列表", tags=["客户表"])
async def get_rebot_customer_list(p: params.RebotCustomerParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.RebotCustomerDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/customer", summary="创建客户表", tags=["客户表"])
async def create_rebot_customer(data: schemas.RebotCustomer, db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.RebotCustomerDal(db).create_data(data=data))


@app.delete("/customer", summary="删除客户表", description="硬删除", tags=["客户表"])
async def delete_rebot_customer_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.RebotCustomerDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/customer/{data_id}", summary="更新客户表", tags=["客户表"])
async def put_rebot_customer(data_id: int, data: schemas.RebotCustomer, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.RebotCustomerDal(auth.db).put_data(data_id, data))


@app.get("/customer/{data_id}", summary="获取客户表信息", tags=["客户表"])
async def get_rebot_customer(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.RebotCustomerSimpleOut
    return SuccessResponse(await crud.RebotCustomerDal(db).get_data(data_id, v_schema=schema))


@app.get("/phone", summary="获取客户表信息", tags=["客户表"])
async def get_rebot_customer(customer_phone: str = Query(None, description="客户手机号"),
                             customer_name: str = Query(None, description="客户姓名"),
                             db: AsyncSession = Depends(db_getter)):
    schema = schemas.RebotCustomerSimpleOut
    if customer_phone:
        return SuccessResponse(await crud.RebotCustomerDal(db).get_data(customer_phone=customer_phone, v_schema=schema))
    elif customer_name:
        return SuccessResponse(await crud.RebotCustomerDal(db).get_data(customer_name=customer_name, v_schema=schema))
    else:
        return ErrorResponse("请输入手机号或者名称")


###########################################################
#    历史消息表
###########################################################
@app.get("/message", summary="获取历史消息表列表", tags=["历史消息表"])
async def get_rebot_customer_message_list(p: params.RebotCustomerMessageParams = Depends(),
                                          auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.RebotCustomerMessageDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/message", summary="创建历史消息表", tags=["历史消息表"])
async def create_rebot_customer_message(data: schemas.AddRebotCustomerMessage, db=Depends(db_getter)):
    customer = await crud.RebotCustomerDal(db).get_data(customer_phone=data.customer_phone, v_return_none=True)
    if customer is None:
        customer_data = data.model_dump()
        d = schemas.RebotCustomer(**customer_data)
        await crud.RebotCustomerDal(db).create_data(data=d)
    message_data = data.model_dump(exclude={'sales_agent_id','tag','summary_content','is_tag_changed',})
    return SuccessResponse(await crud.RebotCustomerMessageDal(db).create_data(data=message_data))


@app.delete("/message", summary="删除历史消息表", description="硬删除", tags=["历史消息表"])
async def delete_rebot_customer_message_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.RebotCustomerMessageDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/message/{data_id}", summary="更新历史消息表", tags=["历史消息表"])
async def put_rebot_customer_message(data_id: int, data: schemas.RebotCustomerMessage,
                                     db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.RebotCustomerMessageDal(db).put_data(data_id, data))


@app.get("/message/{data_id}", summary="获取历史消息表信息", tags=["历史消息表"])
async def get_rebot_customer_message(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.RebotCustomerMessageSimpleOut
    return SuccessResponse(await crud.RebotCustomerMessageDal(db).get_data(data_id, v_schema=schema))


###########################################################
#    业务员配置
###########################################################
@app.get("/sales/agent/config", summary="获取业务员配置列表", tags=["业务员配置"])
async def get_sales_agent_config_list(p: params.SalesAgentConfigParams = Depends(),
                                      auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.SalesAgentConfigDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/sales/agent/config", summary="创建业务员配置", tags=["业务员配置"])
async def create_sales_agent_config(data: schemas.SalesAgentConfig, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.SalesAgentConfigDal(auth.db).create_data(data=data))


@app.delete("/sales/agent/config", summary="删除业务员配置", description="硬删除", tags=["业务员配置"])
async def delete_sales_agent_config_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.SalesAgentConfigDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/sales/agent/config/{data_id}", summary="更新业务员配置", tags=["业务员配置"])
async def put_sales_agent_config(data_id: int, data: schemas.SalesAgentConfig, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.SalesAgentConfigDal(auth.db).put_data(data_id, data))


@app.get("/sales/agent/config/{data_id}", summary="获取业务员配置信息", tags=["业务员配置"])
async def get_sales_agent_config(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.SalesAgentConfigSimpleOut
    return SuccessResponse(await crud.SalesAgentConfigDal(db).get_data(data_id, v_schema=schema))


###########################################################
#    业务员工作流程
###########################################################
@app.get("/sales/agent/workflow", summary="获取业务员工作流程列表", tags=["业务员工作流程"])
async def get_sales_agent_workflow_list(p: params.SalesAgentWorkflowParams = Depends(),
                                        auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.SalesAgentWorkflowDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/sales/agent/workflow", summary="创建业务员工作流程", tags=["业务员工作流程"])
async def create_sales_agent_workflow(data: schemas.SalesAgentWorkflow, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.SalesAgentWorkflowDal(auth.db).create_data(data=data))


@app.delete("/sales/agent/workflow", summary="删除业务员工作流程", description="硬删除", tags=["业务员工作流程"])
async def delete_sales_agent_workflow_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.SalesAgentWorkflowDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/sales/agent/workflow/{data_id}", summary="更新业务员工作流程", tags=["业务员工作流程"])
async def put_sales_agent_workflow(data_id: int, data: schemas.SalesAgentWorkflow, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.SalesAgentWorkflowDal(auth.db).put_data(data_id, data))


@app.get("/sales/agent/workflow/{data_id}", summary="获取业务员工作流程信息", tags=["业务员工作流程"])
async def get_sales_agent_workflow(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.SalesAgentWorkflowSimpleOut
    return SuccessResponse(await crud.SalesAgentWorkflowDal(db).get_data(data_id, v_schema=schema))
