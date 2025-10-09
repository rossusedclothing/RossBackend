#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
# @File           : codes.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Codes(BaseModel):
    code: str = Field(..., title="激活码")
    type: str = Field("trial", title="类型：trial-试用, personal-个人, team-团队, enterprise-企业")
    status: str = Field("active", title="状态：active-未使用, used-已使用, expired-已过期, revoked-已撤销")
    user_limit: int = Field(1, title="用户数量限制")
    duration_days: int = Field(30, title="有效期天数")
    features: str | None = Field(None, title="功能权限配置")
    created_by: str | None = Field(None, title="创建者")
    activated_by: str | None = Field(None, title="激活者")
    activated_datetime: datetime | None = Field(None, title="激活时间")
    expires_datetime: datetime | None = Field(None, title="过期时间")


class CodesSimpleOut(Codes):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
