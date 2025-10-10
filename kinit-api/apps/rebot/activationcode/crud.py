#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from apps.rebot.activationcode import schemas
from apps.rebot.activationcode.models.activation_codes import RossActivationCodes, RossActivationRecords
from core.crud import DalBase
from utils.response import ErrorResponse, SuccessResponse


class CodesDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(CodesDal, self).__init__()
        self.db = db
        self.model = RossActivationCodes
        self.schema = schemas.CodesSimpleOut

    async def check_code(self, code: str):
        if not code:
            return ErrorResponse("请输入注册码|激活码")
        data: RossActivationCodes = await self.get_data(code=code)
        if not data:
            return ErrorResponse("激活码不存在")
        # 检查是否过期
        result = {
            "expires_datetime": data.expires_datetime,
            "activated_datetime": data.activated_datetime
        }
        if data.expires_datetime < datetime.datetime.now():
            result["is_expires"] = True
        else:
            result["is_expires"] = False
        return SuccessResponse(result)


class RecordsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RecordsDal, self).__init__()
        self.db = db
        self.model = RossActivationRecords
        self.schema = schemas.RecordsSimpleOut
