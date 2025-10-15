#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/15 11:38
# @File           : sales_agent_workflow.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class SalesAgentWorkflow(BaseModel):
    phone: str | None = Field(None, title="手机号")
    name: str | None = Field(None, title="名称")
    description: str | None = Field(None, title="描述")
    config: str | None = Field(None, title="配置信息")


class SalesAgentWorkflowSimpleOut(SalesAgentWorkflow):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
