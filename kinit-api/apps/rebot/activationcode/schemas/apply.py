#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/13 13:14
# @File           : apply.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Apply(BaseModel):
    user_name: str | None = Field(None, title="用户名")
    contact: str | None = Field(None, title="联系方式")
    code_id: int | None = Field(None, title="激活码ID")


class ApplySimpleOut(Apply):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
