#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 18:39
# @File           : appUpdate.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Appupdate(BaseModel):
    app_name: str = Field(..., title="app名称")
    version: str = Field(..., title="版本号")
    update_json: str = Field(..., title="更新json")
    desc: str | None = Field(None, title="更新内容")


class AppupdateSimpleOut(Appupdate):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
