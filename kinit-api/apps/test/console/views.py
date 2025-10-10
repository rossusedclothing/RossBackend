#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/10 23:01
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from . import models, schemas, crud, params
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter


app = APIRouter()


###########################################################
#    测试控制台
###########################################################
@app.get("/test/console", summary="获取测试控制台列表", tags=["测试控制台"])
async def get_test_console_list(p: params.TestConsoleParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.TestConsoleDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/test/console", summary="创建测试控制台", tags=["测试控制台"])
async def create_test_console(data: schemas.TestConsole, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.TestConsoleDal(auth.db).create_data(data=data))


@app.delete("/test/console", summary="删除测试控制台", description="硬删除", tags=["测试控制台"])
async def delete_test_console_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.TestConsoleDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/test/console/{data_id}", summary="更新测试控制台", tags=["测试控制台"])
async def put_test_console(data_id: int, data: schemas.TestConsole, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.TestConsoleDal(auth.db).put_data(data_id, data))


@app.get("/test/console/{data_id}", summary="获取测试控制台信息", tags=["测试控制台"])
async def get_test_console(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.TestConsoleSimpleOut
    return SuccessResponse(await crud.TestConsoleDal(db).get_data(data_id, v_schema=schema))

