#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/10 23:01
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class TestConsoleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(TestConsoleDal, self).__init__()
        self.db = db
        self.model = models.Console
        self.schema = schemas.TestConsoleSimpleOut
