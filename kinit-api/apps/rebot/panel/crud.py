#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 16:28
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from apps.rebot.panel.models.panel import AppUpdate, Feedback, ApiKeys
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas




class ApikeysDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ApikeysDal, self).__init__()
        self.db = db
        self.model = ApiKeys
        self.schema = schemas.ApikeysSimpleOut


class AppfeedbackDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(AppfeedbackDal, self).__init__()
        self.db = db
        self.model = Feedback
        self.schema = schemas.AppfeedbackSimpleOut



class AppupdateDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(AppupdateDal, self).__init__()
        self.db = db
        self.model = AppUpdate
        self.schema = schemas.AppupdateSimpleOut
