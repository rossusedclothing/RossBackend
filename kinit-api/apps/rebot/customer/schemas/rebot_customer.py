#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/15 11:36
# @File           : rebot_customer.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class RebotCustomer(BaseModel):
    sales_agent_id: int | None = Field(1, title="所属业务员")
    customer_phone: str | None = Field(None, title="客户手机号")
    customer_name: str | None = Field(None, title="客户名称")
    platform: str | None = Field("whatsapp", title="平台")
    meta_data: str | None = Field(None, title="元数据")
    tag: str | None = Field(None, title="标签")
    is_tag_changed: int | None = Field(0, title="是否修改标签: 0-否 1-是")
    summary_content: str | None = Field(None, title="近期聊天总结")



class RebotCustomerSimpleOut(RebotCustomer):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
