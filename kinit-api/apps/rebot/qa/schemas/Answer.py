#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 11:57
# @File           : Answer.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Answer(BaseModel):
    question_id: int = Field(..., title="问题ID")
    next_question: int | None = Field(None, title="下一题")
    answer: str = Field("", title="答案")


class AnswerSimpleOut(Answer):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
