#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/30 09:59
# @File           : fb_message.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict

from core.data_types import DatetimeStr


class FbMessage(BaseModel):
    message_id: str = Field(..., title="Facebook 消息ID")
    type: str = Field(..., title="消息类型，如 text/image/postback 等")
    content: str = Field(..., title="消息内容")
    status: str = Field("received", title="消息状态，如 received/sent/read 等")
    meta_data: str | None = Field(None, title="消息元数据（如附件、按钮参数等）")
    sender_id: str = Field(..., title="发送者ID（用户PSID）")
    recipient_id: str = Field(..., title="接收者ID（页面ID）")


class FbMessageSimpleOut(FbMessage):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
