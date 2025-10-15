#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/15 11:36
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import schemas, models



class RebotCustomerDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RebotCustomerDal, self).__init__()
        self.db = db
        self.model = models.ReBotCustomer
        self.schema = schemas.RebotCustomerSimpleOut


class RebotCustomerMessageDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RebotCustomerMessageDal, self).__init__()
        self.db = db
        self.model = models.ReBotCustomerMessage
        self.schema = schemas.RebotCustomerMessageSimpleOut


class SalesAgentConfigDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SalesAgentConfigDal, self).__init__()
        self.db = db
        self.model = models.SalesAgentConfig
        self.schema = schemas.SalesAgentConfigSimpleOut


class SalesAgentWorkflowDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SalesAgentWorkflowDal, self).__init__()
        self.db = db
        self.model = models.SalesAgentWorkflow
        self.schema = schemas.SalesAgentWorkflowSimpleOut
