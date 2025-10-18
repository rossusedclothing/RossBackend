#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/15 11:36
# @File           : rebot_customer_message.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class RebotCustomerMessage(BaseModel):
    customer_phone: str | None = Field(None, title="客户手机号")
    customer_name: str | None = Field(None, title="客户名称")
    customer_message: str | None = Field(None, title="客户消息")
    receiver_message: str | None = Field("", title="回复消息")

class AddRebotCustomerMessage(BaseModel):
    sales_agent_id:str | None = Field(None, title="销售代理id")
    customer_phone: str | None = Field(None, title="客户手机号")
    customer_name: str | None = Field(None, title="客户名称")
    customer_message: str | None = Field(None, title="客户消息")
    receiver_message: str | None = Field("", title="回复消息")
    tag: str | None = Field(None, title="标签")
    is_tag_changed: int | None = Field(0, title="是否修改标签: 0-否 1-是")
    summary_content: str | None = Field(None, title="近期聊天总结")


class RebotCustomerMessageSimpleOut(RebotCustomerMessage):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
