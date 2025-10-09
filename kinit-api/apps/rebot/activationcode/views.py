#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
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
from .params.codes import generate_activation_code

app = APIRouter()


###########################################################
#    注册码|激活码
###########################################################

@app.get("/codes", summary="获取注册码|激活码列表", tags=["注册码|激活码"])
async def get_codes_list(p: params.CodesParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.CodesDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/codes", summary="创建注册码|激活码", tags=["注册码|激活码"])
async def create_codes(data: schemas.Codes, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.CodesDal(auth.db).create_data(data=data))


# 生成激活码
@app.get("/generate/codes", summary="生成注册码|激活码", tags=["注册码|激活码"])
async def get_generate_codes(p: params.GenerateCodesParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    codes = []
    for i in range(p.count):
        code = generate_activation_code(p.code_type, p.prefix)
        codes.append(code)
    return SuccessResponse(data=codes, message=f"{p.count}")


@app.delete("/codes", summary="删除注册码|激活码", description="硬删除", tags=["注册码|激活码"])
async def delete_codes_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.CodesDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/codes/{data_id}", summary="更新注册码|激活码", tags=["注册码|激活码"])
async def put_codes(data_id: int, data: schemas.Codes, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.CodesDal(auth.db).put_data(data_id, data))


@app.get("/codes/{data_id}", summary="获取注册码|激活码信息", tags=["注册码|激活码"])
async def get_codes(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.CodesSimpleOut
    return SuccessResponse(await crud.CodesDal(db).get_data(data_id, v_schema=schema))


###########################################################
#    使用记录
###########################################################
@app.get("/records", summary="获取使用记录列表", tags=["使用记录"])
async def get_records_list(p: params.RecordsParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.RecordsDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/records", summary="创建使用记录", tags=["使用记录"])
async def create_records(data: schemas.AddRecords, auth: Auth = Depends(AllUserAuth())):
    code_infos = await crud.CodesDal(auth.db).get_datas(
        limit=1,
        code=data.code,  # 直接等于查询
        v_return_objs=True
    )
    if len(code_infos) == 0:
        return SuccessResponse(code="1001", message="激活码不存在")
    code_info = code_infos[0]
    data.code_id = code_info.id

    new_records = schemas.Records(
        **data.__dict__,  # 使用 model_dump() 而不是 __dict__
    )
    return SuccessResponse(await crud.RecordsDal(auth.db).create_data(data=new_records))


@app.delete("/records", summary="删除使用记录", description="硬删除", tags=["使用记录"])
async def delete_records_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.RecordsDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/records/{data_id}", summary="更新使用记录", tags=["使用记录"])
async def put_records(data_id: int, data: schemas.Records, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.RecordsDal(auth.db).put_data(data_id, data))


@app.get("/records/{data_id}", summary="获取使用记录信息", tags=["使用记录"])
async def get_records(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.RecordsSimpleOut
    return SuccessResponse(await crud.RecordsDal(db).get_data(data_id, v_schema=schema))
