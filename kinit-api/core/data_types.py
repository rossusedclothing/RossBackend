#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/7/16 12:42
# @File           : data_types.py
# @IDE            : PyCharm
# @desc           : 自定义数据类型

"""
自定义数据类型 - 官方文档：https://docs.pydantic.dev/dev-v2/usage/types/custom/#adding-validation-and-serialization
"""
import datetime
from typing import Annotated, Any
from bson import ObjectId
from pydantic import AfterValidator, PlainSerializer, WithJsonSchema
from .validator import *


# 修改 data_types.py 中的 datetime_str_vali 函数
def datetime_str_vali(value: str | datetime.datetime | int | float | dict):
    """
    日期时间字符串验证
    支持两种格式：YYYY-MM-DD HH:MM:SS（空格分隔）、YYYY-MM-DDTHH:MM:SS（T分隔，ISO格式）
    """
    if isinstance(value, str):
        # 支持两种常见格式，优先尝试 T 分隔（ISO），再尝试空格分隔
        patterns = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
        for pattern in patterns:
            try:
                datetime.datetime.strptime(value, pattern)
                return value
            except ValueError:
                continue  # 一种格式失败，尝试下一种
        # 两种格式都失败，抛出错误
        raise ValueError(f"无效的日期时间字符串：{value}（支持格式：YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DDTHH:MM:SS）")

    elif isinstance(value, datetime.datetime):
        # 若输入是 datetime 对象，统一转为 T 分隔的 ISO 格式（与 crud.py 保持一致）
        return value.isoformat()

    elif isinstance(value, dict):
        # 处理 mongodb 日期时间数据类型（保持原有逻辑）
        date_str = value.get("$date")
        if not date_str:
            raise ValueError("mongodb 日期格式错误，缺少 $date 字段")
        # 支持 mongodb 常见的 ISO 格式（带毫秒和 Z，如 2025-10-16T22:41:37.123Z）
        try:
            # 先移除 Z 后缀，再解析（忽略毫秒）
            datetime_obj = datetime.datetime.strptime(date_str.rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f")
            return datetime_obj.isoformat()  # 转为标准 ISO 格式返回
        except ValueError:
            raise ValueError(f"无效的 mongodb 日期：{date_str}")

    # 其他类型（int/float）直接报错（原有逻辑）
    raise ValueError(f"无效的日期时间类型：{type(value)}（仅支持字符串、datetime 对象、mongodb 日期字典）")

'''#o：
# 实现自定义一个日期时间字符串的数据类型
DatetimeStr = Annotated[
    str | datetime.datetime | int | float | dict,
    AfterValidator(datetime_str_vali),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]
'''
# data_types.py 中修改 DatetimeStr 的定义
DatetimeStr = Annotated[
    str | datetime.datetime | int | float | dict,
    AfterValidator(datetime_str_vali),
    # 关键优化：显式处理序列化，确保输出为标准字符串
    PlainSerializer(
        lambda x: x if isinstance(x, str) else x.isoformat() if isinstance(x, datetime.datetime) else str(x),
        return_type=str
    ),
    WithJsonSchema({'type': 'string', 'format': 'date-time'}, mode='serialization')  # 补充 JSON Schema 格式说明
]

# 实现自定义一个手机号类型
Telephone = Annotated[
    str,
    AfterValidator(lambda x: vali_telephone(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


# 实现自定义一个邮箱类型
Email = Annotated[
    str,
    AfterValidator(lambda x: vali_email(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


def date_str_vali(value: str | datetime.date | int | float):
    """
    日期字符串验证
    如果我传入的是字符串，那么直接返回，如果我传入的是一个日期类型，那么会转为字符串格式后返回
    因为在 pydantic 2.0 中是支持 int 或 float 自动转换类型的，所以我这里添加进去，但是在处理时会使这两种类型报错

    官方文档：https://docs.pydantic.dev/dev-v2/usage/types/datetime/
    """
    if isinstance(value, str):
        pattern = "%Y-%m-%d"
        try:
            datetime.datetime.strptime(value, pattern)
            return value
        except ValueError:
            pass
    elif isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    raise ValueError("无效的日期时间或字符串数据")


# 实现自定义一个日期字符串的数据类型
DateStr = Annotated[
    str | datetime.date | int | float,
    AfterValidator(date_str_vali),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


def object_id_str_vali(value: str | dict | ObjectId):
    """
    官方文档：https://docs.pydantic.dev/dev-v2/usage/types/datetime/
    """
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        return value.get("$oid")
    elif isinstance(value, ObjectId):
        return str(value)
    raise ValueError("无效的 ObjectId 数据类型")


ObjectIdStr = Annotated[
    Any,  # 这里不能直接使用 any，需要使用 typing.Any
    AfterValidator(object_id_str_vali),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]
