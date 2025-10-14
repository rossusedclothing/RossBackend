#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/13 12:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession

from apps.businessform.bform import schemas
from apps.businessform.bform.models.business_form import BusinessForm
from core.crud import DalBase


class BusinessFormDal(DalBase):
    """客户表单数据访问层"""

    def __init__(self, db: AsyncSession):
        super(BusinessFormDal, self).__init__()
        self.db = db
        self.model = BusinessForm
        self.schema = schemas.BusinessFormSimpleOut