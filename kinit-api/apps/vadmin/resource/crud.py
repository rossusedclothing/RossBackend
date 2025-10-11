#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/8/25 13:15
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 简要说明
from . import schemas, models
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase



class ImagesDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ImagesDal, self).__init__()
        self.db = db
        self.model = models.VadminImages
        self.schema = schemas.ImagesSimpleOut


class FilesDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(FilesDal, self).__init__()
        self.db = db
        self.model = models.RossFiles
        self.schema = schemas.FilesSimpleOut



