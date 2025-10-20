#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 11:56
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
from apps.vadmin.auth.utils.validation.auth import Auth
from fastapi import Depends, APIRouter
from apps.vadmin.auth.utils.current import AllUserAuth
from core.database import db_getter
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import models, schemas, crud, params



app = APIRouter()


###########################################################
#    问答配置
###########################################################
@app.get("/question", summary="获取问答配置列表", tags=["问答配置"])
async def get_question_list(p: params.QuestionParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.QuestionDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/question", summary="创建问答配置", tags=["问答配置"])
async def create_question(data: schemas.Question, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.QuestionDal(auth.db).create_data(data=data))


@app.delete("/question", summary="删除问答配置", description="硬删除", tags=["问答配置"])
async def delete_question_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.QuestionDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/question/{data_id}", summary="更新问答配置", tags=["问答配置"])
async def put_question(data_id: int, data: schemas.Question, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.QuestionDal(auth.db).put_data(data_id, data))


@app.get("/question/{data_id}", summary="获取问答配置信息", tags=["问答配置"])
async def get_question(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.QuestionSimpleOut
    return SuccessResponse(await crud.QuestionDal(db).get_data(data_id, v_schema=schema))




###########################################################
#    问答配置
###########################################################
@app.get("/answer", summary="获取回答配置列表", tags=["问答配置"])
async def get_Answer_list(p: params.AnswerParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.AnswerDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/answer", summary="创建回答配置", tags=["问答配置"])
async def create_Answer(data: schemas.Answer, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.AnswerDal(auth.db).create_data(data=data))


@app.delete("/answer", summary="删除回答配置", description="硬删除", tags=["问答配置"])
async def delete_Answer_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.AnswerDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/answer/{data_id}", summary="更新回答配置", tags=["问答配置"])
async def put_Answer(data_id: int, data: schemas.Answer, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.AnswerDal(auth.db).put_data(data_id, data))


@app.get("/answer/{data_id}", summary="获取回答配置信息", tags=["问答配置"])
async def get_Answer(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.AnswerSimpleOut
    return SuccessResponse(await crud.AnswerDal(db).get_data(data_id, v_schema=schema))






###########################################################
#    问题模板
###########################################################
@app.get("/template", summary="获取问题模板列表", tags=["问题模板"])
async def get_question_template_list(p: params.QuestionTemplateParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.QuestionTemplateDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/template", summary="创建问题模板", tags=["问题模板"])
async def create_question_template(data: schemas.QuestionTemplate, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.QuestionTemplateDal(auth.db).create_data(data=data))


@app.delete("/template", summary="删除问题模板", description="硬删除", tags=["问题模板"])
async def delete_question_template_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.QuestionTemplateDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/template/{data_id}", summary="更新问题模板", tags=["问题模板"])
async def put_question_template(data_id: int, data: schemas.QuestionTemplate, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.QuestionTemplateDal(auth.db).put_data(data_id, data))


@app.get("/template/{data_id}", summary="获取问题模板信息", tags=["问题模板"])
async def get_question_template(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.QuestionTemplateSimpleOut
    return SuccessResponse(await crud.QuestionTemplateDal(db).get_data(data_id, v_schema=schema))

