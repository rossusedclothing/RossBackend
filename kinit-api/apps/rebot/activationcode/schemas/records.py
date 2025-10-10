#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:19
# @File           : records.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class Records(BaseModel):
    code_id: int = Field(None, title="激活码ID", )
    user_id: str = Field(..., title="用户ID")
    device_id: str | None = Field(None, title="设备ID")
    device_info: str | None = Field(None, title="设备信息")
    ip_address: str | None = Field(None, title="IP地址")
    activated_datetime: datetime = Field(..., title="激活时间")
    last_verified_datetime: datetime | None = Field(None, title="最后验证时间")
    status: str = Field("active", title="状态：active-有效, expired-过期, revoked-撤销")


class RecordsSimpleOut(Records):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")

    # create_datetime: DatetimeStr = Field(..., title="创建时间")
    # update_datetime: DatetimeStr = Field(..., title="更新时间")


class AddRecords(BaseModel):
    code: str = Field(..., title="激活码")
    code_id: int = Field(None, title="激活码ID", )
    user_id: str = Field(None, title="用户ID")
    user_limit: int = Field(1, title="激活次数")
    device_id: str | None = Field(None, title="设备ID")
    device_info: str | None = Field(None, title="设备信息")
    ip_address: str | None = Field(None, title="IP地址")
    activated_datetime:datetime | None = Field(datetime.now(), title="激活时间")
    last_verified_datetime: datetime | None = Field(datetime.now(), title="最后验证时间")
    status: str = Field("active", title="状态：active-有效, expired-过期, revoked-撤销")