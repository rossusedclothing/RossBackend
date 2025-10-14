#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
# @File           : business_form.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作    #序列化模式文件

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from core.data_types import DatetimeStr


class BusinessForm(BaseModel):
    """客户表单基础模型"""
    name: str = Field(..., max_length=50, title="名字")
    position: Optional[str] = Field(None, max_length=50, title="职位")
    region: str = Field(..., max_length=100, title="地区")
    factory_spec: Optional[str] = Field(None, max_length=200, title="工厂规格")
    product: str = Field(..., max_length=100, title="产品")
    website: Optional[str] = Field(None, max_length=200, title="网站链接")
    has_export_experience: bool = Field(False, title="有没有做过外贸")
    export_market: Optional[str] = Field(None, max_length=200, title="产品出口市场")
    student_identity: Optional[str] = Field(None, max_length=50, title="学员身份")
    num_members_tradeteam: int = Field(0, ge=0, title="外贸团队人数")
    company_size: Optional[str] = Field(None, max_length=50, title="公司人数规模")


class BusinessFormSimpleOut(BusinessForm):
    """客户表单简单输出模型"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class BusinessFormCreate(BusinessForm):
    """创建客户表单模型"""
    pass


class BusinessFormUpdate(BaseModel):
    """更新客户表单模型"""
    name: Optional[str] = Field(None, max_length=50, title="名字")
    position: Optional[str] = Field(None, max_length=50, title="职位")
    region: Optional[str] = Field(None, max_length=100, title="地区")
    factory_spec: Optional[str] = Field(None, max_length=200, title="工厂规格")
    product: Optional[str] = Field(None, max_length=100, title="产品")
    website: Optional[str] = Field(None, max_length=200, title="网站链接")
    has_export_experience: Optional[bool] = Field(None, title="有没有做过外贸")
    export_market: Optional[str] = Field(None, max_length=200, title="产品出口市场")
    student_identity: Optional[str] = Field(None, max_length=50, title="学员身份")
    num_members_tradeteam: Optional[int] = Field(None, ge=0, title="外贸团队人数")
    company_size: Optional[str] = Field(None, max_length=50, title="公司人数规模")