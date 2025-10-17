#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/13 16:19
# @File           : business_form.py
# @IDE            : PyCharm
# @desc           : 客户表单查询参数

from typing import Optional
from fastapi import Depends, Query

from core.dependencies import Paging, QueryParams


class BusinessFormParams(QueryParams):
    """客户表单查询参数"""
    
    def __init__(
        self,
        name: Optional[str] = Query(None, description="姓名"),
        position: Optional[str] = Query(None, description="职位"),
        region: Optional[str] = Query(None, description="地区"),
        product: Optional[str] = Query(None, description="产品"),
        has_export_experience: Optional[bool] = Query(None, description="是否有外贸经验"),
        student_identity: Optional[str] = Query(None, description="学员身份"),
        company_size: Optional[str] = Query(None, description="公司规模"),
        bt: Optional[int] = Query(None, description="分享人用户ID"),  # 新增 bt 参数
        params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = name
        self.position = position
        self.region = region
        self.product = product
        self.has_export_experience = has_export_experience
        self.student_identity = student_identity
        self.company_size = company_size
        self.bt = bt  # 新增