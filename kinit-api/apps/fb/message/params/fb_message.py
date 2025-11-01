#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/30 09:59
# @File           : fb_message.py
# @IDE            : PyCharm
# @desc           : facebook message

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class FbMessageParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
