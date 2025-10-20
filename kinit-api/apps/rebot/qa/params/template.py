#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/19 18:18
# @File           : template.py
# @IDE            : PyCharm
# @desc           : 问题模板

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class QuestionTemplateParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
