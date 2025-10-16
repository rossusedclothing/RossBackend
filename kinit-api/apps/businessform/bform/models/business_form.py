#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
# @File           : business_form.py
# @IDE            : PyCharm
# @desc           : 客户表单数据模型

from sqlalchemy import String, Integer, Column,DateTime, Boolean, func
from sqlalchemy.orm import mapped_column, Mapped
from typing import Optional
from datetime import datetime  # 导入 Python 标准库的 datetime 类型

from core.database import Base


class BusinessForm(Base):
    """客户表单模型"""
    __tablename__ = "business_form"

    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键')
    name = mapped_column(String(50), nullable=False, comment='名字')
    position = mapped_column(String(50), nullable=True, comment='职位')
    region = mapped_column(String(100), nullable=False, comment='地区')
    factory_spec = mapped_column(String(200), nullable=True, comment='工厂规格')
    product = mapped_column(String(100), nullable=False, comment='产品')
    website = mapped_column(String(200), nullable=True, comment='网站链接')
    has_export_experience = mapped_column(Boolean, nullable=True, default=False, comment='有没有做过外贸')
    export_market = mapped_column(String(200), nullable=True, comment='产品出口市场')
    student_identity = mapped_column(String(50), nullable=True, comment='学员身份')
    num_members_tradeteam = mapped_column(Integer, nullable=True, default=0, comment='外贸团队人数')
    company_size = mapped_column(String(50), nullable=True, comment='公司人数规模')
    # 可选：若需前端传递，添加该字段（默认0，与数据库默认值一致）
    #B：is_delete: Optional[int] = Field(0, ge=0, le=1, title="是否删除：0-否，1-是")
    # 修正 is_delete 字段的定义（移除 Field，使用 SQLAlchemy 参数）
    # 核心修复1：将 create_datetime 改为 mapped_column + 类型注解
    create_datetime: Mapped[Optional[datetime]] = mapped_column(
       DateTime,
       default=func.now(),  # 自动填充创建时间
       comment="创建时间"
    )

    # 核心修复2：将 update_datetime 改为 mapped_column + 类型注解
    update_datetime: Mapped[Optional[datetime]] = mapped_column(
       DateTime,
       default=func.now(),
       onupdate=func.now(),  # 更新时自动刷新
       comment="更新时间"
    )

    # is_delete 字段已正确使用 mapped_column，保持不变
    is_delete: Mapped[Optional[int]] = mapped_column(
       Integer,
       default=0,
       nullable=True,
       comment="是否删除：0-否，1-是"
    )