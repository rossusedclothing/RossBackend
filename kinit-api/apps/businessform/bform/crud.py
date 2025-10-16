#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/13 12:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # 用于查询（可选，按需添加）

from apps.businessform.bform import schemas
from apps.businessform.bform.models.business_form import BusinessForm
from core.crud import DalBase


class BusinessFormDal(DalBase):
    """客户表单数据访问层"""

    def __init__(self, db: AsyncSession):
        super(BusinessFormDal, self).__init__()
        self.db = db  # 数据库会话
        self.model = BusinessForm  # 关联的数据库模型
        self.schema = schemas.BusinessFormSimpleOut  # 输出的 Pydantic 模型

    async def create_data(self, data: schemas.BusinessFormCreate):
        """
        创建客户表单数据
        :param data: 前端传递的创建参数（Pydantic 模型）
        :return: 创建成功后的完整数据（字典格式，确保可 JSON 序列化）
        """
        # 1. 将 Pydantic 输入模型转换为数据库模型实例
        db_instance = self.model(**data.model_dump())

        # 2. 将实例添加到数据库会话
        self.db.add(db_instance)

        # 3. 强制会话同步，确保实例状态被数据库识别（获取临时 ID 和默认值）
        await self.db.flush()

        # 4. 刷新会话，获取数据库自动生成的完整字段（id、create_datetime 等）
        await self.db.refresh(db_instance)

        # 5. 转换为 Pydantic 输出模型实例
        pydantic_instance = self.schema.from_orm(db_instance)

        # 6. 关键：手动将 Pydantic 实例转为字典，确保无不可序列化属性
        # model_dump() 会自动处理所有字段的序列化（包括 DatetimeStr 转为字符串）
        return pydantic_instance.model_dump()