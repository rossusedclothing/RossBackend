#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 18:30
# @File           : files.py
# @IDE            : PyCharm
# @desc           : 文件资源

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class FilesParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
