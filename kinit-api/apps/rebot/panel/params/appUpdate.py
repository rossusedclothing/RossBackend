#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 18:39
# @File           : appUpdate.py
# @IDE            : PyCharm
# @desc           : App更新

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class AppupdateParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
