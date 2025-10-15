#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/13 13:14
# @File           : apply.py
# @IDE            : PyCharm
# @desc           : 申请激活码

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class ApplyParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
