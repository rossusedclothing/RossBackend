#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/11 16:29
# @File           : appFeedback.py
# @IDE            : PyCharm
# @desc           : App问题反馈

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class AppfeedbackParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
