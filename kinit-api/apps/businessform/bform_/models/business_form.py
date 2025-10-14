#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
# @File           : business_form.py
# @IDE            : PyCharm
# @desc           : 客户表单数据模型

from sqlalchemy import String, Integer, DateTime, Boolean, func
from sqlalchemy.orm import mapped_column

from core.database import Base


class BusinessForm(Base):
    """客户表单模型"""
    __tablename__ = "business_form"

    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键')
    name = mapped_column(String(50), nullable=False, comment='名字')
    position = mapped_column(String(50), nullable=False, comment='职位')
    region = mapped_column(String(100), nullable=False, comment='地区')
    factory_spec = mapped_column(String(200), nullable=False, comment='工厂规格')
    product = mapped_column(String(100), nullable=False, comment='产品')
    website = mapped_column(String(200), nullable=True, comment='网站链接')
    has_export_experience = mapped_column(Boolean, nullable=False, default=False, comment='有没有做过外贸')
    export_market = mapped_column(String(200), nullable=False, comment='产品出口市场')
    student_identity = mapped_column(String(50), nullable=False, comment='学员身份')
    num_members_tradeteam = mapped_column(Integer, nullable=False, default=0, comment='外贸团队人数')
    company_size = mapped_column(String(50), nullable=False, comment='公司人数规模')
    create_datetime = mapped_column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    update_datetime = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    is_delete = mapped_column(Integer, nullable=False, default=0, comment='是否删除：0-否, 1-是')