#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/30 09:59
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
import asyncio
from contextlib import asynccontextmanager

import aioredis
from fastapi import APIRouter, Depends, Request, HTTPException, FastAPI
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import PlainTextResponse

from application.settings import FB_VERIFY_TOKEN
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter, redis_getter
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import schemas, crud, params

app = APIRouter()


###########################################################
#    facebook webhook
###########################################################
@app.get("/webhook", summary="facebook webhook verify", tags=["facebook webhook"])
async def fb_webhook_verify(request: Request, db: AsyncSession = Depends(db_getter)):
    """
    Facebook 用 GET 请求验证 webhook。
    示例：
      curl -X GET "localhost:1337/webhook?hub.verify_token=YOUR-VERIFY-TOKEN&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe"
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == FB_VERIFY_TOKEN:
        # 验证通过，返回 challenge
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        raise HTTPException(status_code=403, detail="Verification token mismatch")


@app.post("/webhook", summary="facebook webhook event", tags=["facebook webhook"])
async def fb_webhook_event(request: Request, db: AsyncSession = Depends(db_getter),
                           redis: Redis = Depends(redis_getter)):
    # TODO 处理传入消息
    # TODO 发送消息
    pass


###########################################################
#    facebook message
###########################################################
@app.get("/message", summary="获取facebook message列表", tags=["facebook message"])
async def get_fb_message_list(p: params.FbMessageParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.FbMessageDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/message", summary="创建facebook message", tags=["facebook message"])
async def create_fb_message(data: schemas.FbMessage, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.FbMessageDal(auth.db).create_data(data=data))


@app.delete("/message", summary="删除facebook message", description="硬删除", tags=["facebook message"])
async def delete_fb_message_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.FbMessageDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/message/{data_id}", summary="更新facebook message", tags=["facebook message"])
async def put_fb_message(data_id: int, data: schemas.FbMessage, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.FbMessageDal(auth.db).put_data(data_id, data))


@app.get("/message/{data_id}", summary="获取facebook message信息", tags=["facebook message"])
async def get_fb_message(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.FbMessageSimpleOut
    return SuccessResponse(await crud.FbMessageDal(db).get_data(data_id, v_schema=schema))
