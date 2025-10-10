#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/10 23:01
# @File           : test_console.py
# @IDE            : PyCharm
# @desc           : 测试控制台

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class TestConsoleParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
