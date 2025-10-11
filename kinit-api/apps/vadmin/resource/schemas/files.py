#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 18:30
# @File           : files.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Files(BaseModel):
    filename: str = Field(..., title="原始文件名称")
    storage_name: str = Field(..., title="存储文件名称")
    file_path: str = Field(..., title="文件存储路径")
    file_url: str = Field(..., title="文件访问URL")
    md5: str = Field(..., title="文件MD5哈希值")
    file_size: int = Field(..., title="文件大小(MB)")
    file_type: str = Field(..., title="文件MIME类型")
    file_extension: str = Field(..., title="文件扩展名")
    uploader_id: int | None = Field(None, title="上传用户ID")
    app_name: str | None = Field(None, title="关联应用名称")
    category: str | None = Field(None, title="文件分类")
    status: str | None = Field("active", title="文件状态: active/inactive/deleted")
    is_public: bool | None = Field(False, title="是否公开访问")


class FilesSimpleOut(Files):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
