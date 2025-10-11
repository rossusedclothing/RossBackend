from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
import sys

from core.database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# 添加当前项目路径到环境变量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 导入项目中的基本映射类，与 需要迁移的 ORM 模型
# from apps.vadmin.auth.models import *
# from apps.vadmin.system.models import *
# from apps.vadmin.record.models import *
# from apps.vadmin.help.models import *
# from apps.vadmin.resource.models import *
# from apps.rebot.qa.models import *
# from apps.test.console.models import *

from apps.rebot.panel.models import *

# 修改配置中的参数
target_metadata = Base.metadata


# 过滤函数 - 只迁移指定的表
def include_object(object, name, type_, reflected, compare_to):
    """
    过滤要迁移的对象
    """
    # 只处理表类型的对象
    if type_ == "table":
        # 只包含以 'ross_panel' 开头的表
        if name.startswith('ross_panel'):
            print(f"包含表: {name}")  # 调试信息
            return True
        else:
            print(f"排除表: {name}")  # 调试信息
            return False

    # 对于非表对象（索引、约束等），默认包含
    return True


def run_migrations_offline():
    """
    以"脱机"模式运行迁移。
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # 是否检查字段类型，字段长度
        compare_server_default=True,  # 是否比较在数据库中的默认值
        include_object=include_object  # 添加过滤函数
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    以"在线"模式运行迁移。
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # 是否检查字段类型，字段长度
            compare_server_default=True,  # 是否比较在数据库中的默认值
            include_object=include_object  # 添加过滤函数
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("offline")
    run_migrations_offline()
else:
    print("online")
    run_migrations_online()