#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 11:56
# @File           : question.py
# @IDE            : PyCharm
# @desc           : 问答配置

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class QuestionParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
