#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 11:56
# @File           : question.py
# @IDE            : PyCharm
# @desc           : 问答配置

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class QuestionParams(QueryParams):
    def __init__(self,
                 template_id: int | None = Query(None, title="问题模板ID"),
                 question: str | None = Query(None, title="问题"),
                 params: Paging = Depends()):
        super().__init__(params)
        self.template_id = ("eq", template_id)
        if question:
            self.question = ("like", question)
