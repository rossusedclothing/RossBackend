#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/19 18:18
# @File           : template.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class QuestionTemplate(BaseModel):
    title: str = Field("", title="标题")
    description: str = Field("", title="描述")
    status: int = Field(1, title="状态")
    sale_agent_id: int = Field(0, title="售前代理ID")


class QuestionTemplateSimpleOut(QuestionTemplate):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
