#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 16:28
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import crud, schemas, params

app = APIRouter()


###########################################################
#    Apikey管理
###########################################################
@app.get("/apiKeys", summary="获取Apikey管理列表", tags=["Apikey管理"])
async def get_apiKeys_list(p: params.ApikeysParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.ApikeysDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/apiKeys", summary="创建Apikey管理", tags=["Apikey管理"])
async def create_apiKeys(data: schemas.Apikeys, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.ApikeysDal(auth.db).create_data(data=data))


@app.delete("/apiKeys", summary="删除Apikey管理", description="硬删除", tags=["Apikey管理"])
async def delete_apiKeys_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.ApikeysDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/apiKeys/{data_id}", summary="更新Apikey管理", tags=["Apikey管理"])
async def put_apiKeys(data_id: int, data: schemas.Apikeys, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.ApikeysDal(auth.db).put_data(data_id, data))


@app.get("/apiKeys/{data_id}", summary="获取Apikey管理信息", tags=["Apikey管理"])
async def get_apiKeys(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.ApikeysSimpleOut
    return SuccessResponse(await crud.ApikeysDal(db).get_data(data_id, v_schema=schema))


###########################################################
#    App问题反馈
###########################################################
@app.get("/appFeedback", summary="获取App问题反馈列表", tags=["App问题反馈"])
async def get_appFeedback_list(p: params.AppfeedbackParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.AppfeedbackDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/appFeedback", summary="创建App问题反馈", tags=["App问题反馈"])
async def create_appFeedback(data: schemas.Appfeedback,
                             db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.AppfeedbackDal(db).create_data(data=data))


@app.delete("/appFeedback", summary="删除App问题反馈", description="硬删除", tags=["App问题反馈"])
async def delete_appFeedback_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.AppfeedbackDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/appFeedback/{data_id}", summary="更新App问题反馈", tags=["App问题反馈"])
async def put_appFeedback(data_id: int, data: schemas.Appfeedback, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.AppfeedbackDal(auth.db).put_data(data_id, data))


@app.get("/appFeedback/{data_id}", summary="获取App问题反馈信息", tags=["App问题反馈"])
async def get_appFeedback(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.AppfeedbackSimpleOut
    return SuccessResponse(await crud.AppfeedbackDal(db).get_data(data_id, v_schema=schema))


###########################################################
#    App更新
###########################################################
@app.get("/appUpdate", summary="获取App更新列表", tags=["App更新"])
async def get_appUpdate_list(p: params.AppupdateParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas, count = await crud.AppupdateDal(db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/appUpdate", summary="创建App更新", tags=["App更新"])
async def create_appUpdate(data: schemas.Appupdate, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.AppupdateDal(auth.db).create_data(data=data))


@app.delete("/appUpdate", summary="删除App更新", description="硬删除", tags=["App更新"])
async def delete_appUpdate_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.AppupdateDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/appUpdate/{data_id}", summary="更新App更新", tags=["App更新"])
async def put_appUpdate(data_id: int, data: schemas.Appupdate, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.AppupdateDal(auth.db).put_data(data_id, data))


@app.get("/appUpdate/{data_id}", summary="获取App更新信息", tags=["App更新"])
async def get_appUpdate(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.AppupdateSimpleOut
    return SuccessResponse(await crud.AppupdateDal(db).get_data(data_id, v_schema=schema))
