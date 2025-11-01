#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/30 09:59
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class FbMessageDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(FbMessageDal, self).__init__()
        self.db = db
        self.model = models.FbMessage
        self.schema = schemas.FbMessageSimpleOut
