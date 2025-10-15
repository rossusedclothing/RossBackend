#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
from .params import GenerateCodesParams
from .params.codes import generate_activation_code
from utils.response import ErrorResponse, SuccessResponse
from . import params, crud, models, schemas
from apps.vadmin.auth.utils.validation.auth import Auth
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, Request
from core.database import db_getter
from apps.vadmin.auth.utils.current import AllUserAuth
from core.dependencies import IdList

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


@app.get("/check/codes", summary="检查注册码|激活码", tags=["注册码|激活码"])
async def check_codes(code: str, db: AsyncSession = Depends(db_getter)):
    return await crud.CodesDal(db).check_code(code)


###########################################################
#    使用记录
###########################################################
@app.get("/records", summary="获取使用记录列表", tags=["使用记录"])
async def get_records_list(p: params.RecordsParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.RecordsDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/records", summary="创建使用记录", tags=["使用记录"])
async def create_records(
        request: Request,
        data: schemas.AddRecords,
        db: AsyncSession = Depends(db_getter)):
    code_infos = await crud.CodesDal(db).get_datas(
        limit=1,
        code=data.code,  # 直接等于查询
        v_return_objs=True
    )
    if len(code_infos) == 0:
        return ErrorResponse(message="激活码不存在")
    code_info: schemas.Codes = code_infos[0]

    # 2. 检查激活码状态（按优先级顺序）
    if code_info.status == "expired":
        return ErrorResponse(message="激活码已过期")
    if "enterprise" not in code_info.type and "team" not in code_info.type and code_info.status == "used":
        return ErrorResponse(message=f"激活码已使用")

    # 3. 检查激活码是否过期
    if code_info.activated_datetime and code_info.duration_days > 0:
        # 判断当前时间是否超过激活码的过期时间
        if code_info.expires_datetime is None:
            code_info.expires_datetime = code_info.activated_datetime + timedelta(days=code_info.duration_days)
        if code_info.expires_datetime < datetime.now():
            # 更新数据库中的状态为过期
            code_info.status = "expired"
            await crud.CodesDal(db).put_data(data_id=code_info.id, data=code_info)
            return ErrorResponse(message=f"激活码已过期:{code_info.activated_datetime} - {code_info.expires_datetime}")

    # 4. 检查使用次数限制（针对scope类型的激活码）
    if "scope" in code_info.type:
        if code_info.user_limit <= 0:
            # 激活码次数已用完
            code_info.status = "used"
            await crud.CodesDal(db).put_data(data_id=code_info.id, data=code_info)
            return ErrorResponse(message="激活码次数已用完")
        if data.user_limit > code_info.user_limit:
            return ErrorResponse(message="激活码次数不足请重新购买！")
        new_user_limit = code_info.user_limit - data.user_limit
        code_info.user_limit = new_user_limit
        code_info.status = "used" if new_user_limit <= 0 else "active"
        # 更新数据库中的
        await crud.CodesDal(db).put_data(data_id=code_info.id, data=code_info)

    # 设置激活码状态为已使用
    if "trial" in code_info.type or "personal" in code_info.type:
        code_info.status = "used"
        code_info.activated_datetime = datetime.now()
        code_info.expires_datetime = datetime.now() + timedelta(days=code_info.duration_days)
        await crud.CodesDal(db).put_data(data_id=code_info.id, data=code_info)

    data.code_id = code_info.id
    data.user_id = data.user_id or "1"
    data.ip_address = request.client.host
    data.device_info = request.headers.get("user-agent", "")
    data.device_id = request.headers.get("device-id", "ROSS-BROWSER-PLUGIN")
    new_records = schemas.Records(
        **data.__dict__,  # 使用 model_dump() 而不是 __dict__
    )
    # 创建使用记录
    await crud.RecordsDal(db).create_data(data=new_records)
    return SuccessResponse(msg="激活成功")


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


###########################################################
#    申请激活码
###########################################################
@app.get("/apply", summary="获取申请激活码列表", tags=["申请激活码"])
async def get_apply_list(p: params.ApplyParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.ApplyDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/apply", summary="创建申请激活码", tags=["申请激活码"])
async def create_apply(data: schemas.Apply, db: AsyncSession = Depends(db_getter)):
    # 查询是否已申请过激活码
    apply_info = await crud.ApplyDal(db).get_data(user_name=data.user_name, contact=data.contact, v_return_none=True)
    if apply_info:
        code_info = await crud.CodesDal(db).get_data(data_id=apply_info.code_id, v_schema=schemas.CodesSimpleOut)
        return SuccessResponse(data=code_info,msg="fail")
    # 创建激活码
    temp_code = generate_activation_code("personal", "ROSS-TEMP")
    codes = schemas.Codes(
        code=temp_code,
        type="personal",
        duration_days=30,
        created_by=data.user_name,
        features=None,
        status="active",
        user_limit=1,
        activated_by=data.user_name)
    new_code = await crud.CodesDal(db).create_data(data=codes)
    data.code_id = new_code.get("id")
    # 创建申请记录
    await crud.ApplyDal(db).create_data(data=data)
    return SuccessResponse(data=new_code, msg="success")


@app.delete("/apply", summary="删除申请激活码", description="硬删除", tags=["申请激活码"])
async def delete_apply_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.ApplyDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/apply/{data_id}", summary="更新申请激活码", tags=["申请激活码"])
async def put_apply(data_id: int, data: schemas.Apply, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.ApplyDal(auth.db).put_data(data_id, data))


@app.get("/apply/{data_id}", summary="获取申请激活码信息", tags=["申请激活码"])
async def get_apply(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.ApplySimpleOut
    return SuccessResponse(await crud.ApplyDal(db).get_data(data_id, v_schema=schema))
