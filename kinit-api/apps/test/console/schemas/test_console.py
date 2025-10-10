#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/10 23:01
# @File           : test_console.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class TestConsole(BaseModel):
    name: str | None = Field(None, title="None")
    description: str | None = Field(None, title="None")
    price: str | None = Field(None, title="None")
    is_active: int | None = Field(None, title="None")


class TestConsoleSimpleOut(TestConsole):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
