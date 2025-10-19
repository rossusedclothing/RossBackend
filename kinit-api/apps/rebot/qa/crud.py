#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 11:56
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from apps.rebot.qa import schemas
from apps.rebot.qa.models.question import RossQuestion, RossAnswer
from . import models, schemas
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession



class QuestionDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(QuestionDal, self).__init__()
        self.db = db
        self.model = RossQuestion
        self.schema = schemas.QuestionSimpleOut


class AnswerDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(AnswerDal, self).__init__()
        self.db = db
        self.model = RossAnswer
        self.schema = schemas.AnswerSimpleOut


class QuestionTemplateDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(QuestionTemplateDal, self).__init__()
        self.db = db
        self.model = models.RossQuestionTemplate
        self.schema = schemas.QuestionTemplateSimpleOut
