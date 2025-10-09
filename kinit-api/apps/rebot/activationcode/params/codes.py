#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/10/09 12:18
# @File           : codes.py
# @IDE            : PyCharm
# @desc           : 注册码|激活码
from typing import Optional

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class CodesParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)




class GenerateCodesParams:
    def __init__(
        self,
        count: int = 1,                    # 生成数量
        code_type: str = "personal",       # 类型: personal/team/enterprise
        duration_days: int = 30,           # 有效期天数
        user_limit: int = 1,               # 用户限制数
        prefix: Optional[str] = None,      # 编码前缀
        features: Optional[str] = None     # 特性配置
    ):
        self.count = count
        self.code_type = code_type
        self.duration_days = duration_days
        self.user_limit = user_limit
        self.prefix = prefix
        self.features = features


def generate_activation_code(code_type: str, prefix: Optional[str] = None) -> str:
    """
    生成随机激活码
    """
    import random
    import string

    # 如果未指定前缀，根据类型生成
    if not prefix:
        if code_type == 'team':
            prefix = 'ROSS-TEAM'
        elif code_type == 'personal':
            prefix = 'ROSS-PERS'
        elif code_type == 'enterprise':
            prefix = 'ROSS-ENT'
        else:
            prefix = 'ROSS-CODE'

    # 生成随机部分（8位数字字母组合）
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    random_part = f"{random_part[:4]}-{random_part[4:]}"

    # 组合成完整激活码
    activation_code = f"{prefix}-{random_part}"

    return activation_code


