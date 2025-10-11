#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 16:28
# @File           : apiKeys.py
# @IDE            : PyCharm
# @desc           : Apikey管理

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class ApikeysParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
