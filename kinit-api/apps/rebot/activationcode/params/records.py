#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:19
# @File           : records.py
# @IDE            : PyCharm
# @desc           : 使用记录

from fastapi import Depends

from core.dependencies import Paging, QueryParams


class RecordsParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
