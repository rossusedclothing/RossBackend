#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/8/25 9:29
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 简要说明
from apps.vadmin.auth.utils.current import FullAdminAuth, AllUserAuth
from fastapi import UploadFile, Depends, APIRouter
from . import crud, params, schemas, models
from core.database import db_getter
from utils.file.aliyun_oss import BucketConf, AliyunOSS
from sqlalchemy.orm import joinedload
from utils.response import SuccessResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import IdList
from application.settings import ALIYUN_OSS
from apps.vadmin.auth.utils.validation.auth import Auth


app = APIRouter()


###########################################################
#    图片资源管理
###########################################################
@app.get("/images", summary="获取图片列表")
async def get_images_list(p: params.ImagesParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.VadminImages
    v_options = [joinedload(model.create_user)]
    v_schema = schemas.ImagesOut
    datas, count = await crud.ImagesDal(auth.db).get_datas(
        **p.dict(),
        v_options=v_options,
        v_schema=v_schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/images", summary="创建图片")
async def create_images(file: UploadFile, auth: Auth = Depends(FullAdminAuth())):
    filepath = f"/resource/images/"
    result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_image(filepath, file)
    data = schemas.Images(
        filename=file.filename,
        image_url=result,
        create_user_id=auth.user.id
    )

    return SuccessResponse(await crud.ImagesDal(auth.db).create_data(data=data))


@app.delete("/images", summary="删除图片", description="硬删除")
async def delete_images(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.ImagesDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.get("/images/{data_id}", summary="获取图片信息")
async def get_images(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ImagesDal(auth.db).get_data(data_id, v_schema=schemas.ImagesSimpleOut))



###########################################################
#    文件资源
###########################################################
@app.get("/files", summary="获取文件资源列表", tags=["文件资源"])
async def get_files_list(p: params.FilesParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.FilesDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/files", summary="创建文件资源", tags=["文件资源"])
async def create_files(data: schemas.Files, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.FilesDal(auth.db).create_data(data=data))


@app.delete("/files", summary="删除文件资源", description="硬删除", tags=["文件资源"])
async def delete_files_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.FilesDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/files/{data_id}", summary="更新文件资源", tags=["文件资源"])
async def put_files(data_id: int, data: schemas.Files, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.FilesDal(auth.db).put_data(data_id, data))


@app.get("/files/{data_id}", summary="获取文件资源信息", tags=["文件资源"])
async def get_files(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.FilesSimpleOut
    return SuccessResponse(await crud.FilesDal(db).get_data(data_id, v_schema=schema))