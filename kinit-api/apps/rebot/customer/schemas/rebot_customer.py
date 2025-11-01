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
    user_tag: str | None = Field(None, title="用户标签")
    summary_content: str | None = Field(None, title="摘要内容")
    sales_repp_phone: str | None = Field(None, title="销售代表手机号")
    sales_agent: str | None = Field(None, title="业务员手机号")
    is_tagged: int | None = Field(0, title="是否打标签 0 未打标签 1 已打标签")
    answering_progress: int | None = Field(1, title="问题进度")




class RebotCustomerSimpleOut(RebotCustomer):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
