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

    async def get_datas(self, **kwargs):
        """
        重写 get_datas 方法以支持 bt 参数
        - 当 bt 为 None 或 0 时，查询所有记录
        - 当 bt 为有效正整数时，按 bt 筛选
        """
        # 从 kwargs 中提取 bt 参数
        bt = kwargs.pop('bt', None)

        # 构建基础查询
        query = select(self.model)

        # 处理 bt 参数：当 bt 为有效正整数时才添加筛选条件
        if bt is not None and bt != 0:
            query = query.where(self.model.bt == bt)

        # 处理分页
        skip = kwargs.get('skip', 0)
        limit = kwargs.get('limit', 100)
        query = query.offset(skip).limit(limit)

        # 执行查询
        result = await self.db.execute(query)
        datas = result.scalars().all()

        # 如果需要返回计数
        if kwargs.get('v_return_count'):
            count_query = select(self.model)
            # 复制 bt 筛选条件：只有当 bt 为有效正整数时才筛选
            if bt is not None and bt != 0:
                count_query = count_query.where(self.model.bt == bt)
            count_result = await self.db.execute(count_query)
            count = len(count_result.scalars().all())
            return [self.schema.from_orm(data).model_dump() for data in datas], count

        return [self.schema.from_orm(data).model_dump() for data in datas]

    # 可选：添加专门的按 bt 查询的方法
    async def get_forms_by_bt(self, bt: int, skip: int = 0, limit: int = 100):
        """
        根据分享人用户ID获取表单列表
        """
        return await self.get_datas(bt=bt, skip=skip, limit=limit)