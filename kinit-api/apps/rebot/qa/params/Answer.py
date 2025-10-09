#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 11:57
# @File           : Answer.py
# @IDE            : PyCharm
# @desc           : 回答配置

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class AnswerParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
