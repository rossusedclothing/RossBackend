#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from sqlalchemy.ext.asyncio import AsyncSession

from apps.rebot.activationcode import schemas
from apps.rebot.activationcode.models.activation_codes import RossActivationCodes, RossActivationRecords
from core.crud import DalBase


class CodesDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(CodesDal, self).__init__()
        self.db = db
        self.model = RossActivationCodes
        self.schema = schemas.CodesSimpleOut


class RecordsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RecordsDal, self).__init__()
        self.db = db
        self.model = RossActivationRecords
        self.schema = schemas.RecordsSimpleOut
