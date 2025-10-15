#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/15 11:37
# @File           : sales_agent_config.py
# @IDE            : PyCharm
# @desc           : 业务员配置

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class SalesAgentConfigParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
