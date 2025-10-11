#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 16:28
# @File           : apiKeys.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Apikeys(BaseModel):
    platform: str = Field(..., title="平台名称")
    key_value: str = Field(..., title="key")
    useapp_name: str = Field(..., title="使用的app名称")
    desc: str | None = Field(None, title="描述")


class ApikeysSimpleOut(Apikeys):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
