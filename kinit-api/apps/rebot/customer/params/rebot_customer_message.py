#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/15 11:36
# @File           : rebot_customer_message.py
# @IDE            : PyCharm
# @desc           : 历史消息表

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class RebotCustomerMessageParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
