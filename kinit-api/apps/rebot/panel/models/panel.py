from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column

from db.db_base import BaseModel


class ApiKeys(BaseModel):
    """
    ross api key
    """
    __tablename__ = "ross_panel_api_keys"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键')
    platform = mapped_column(String(255), nullable=False, comment='平台名称')
    key_value = mapped_column(String(255), nullable=False, unique=True, comment='key')
    useapp_name = mapped_column(String(255), nullable=False, comment='使用的app名称')
    desc = mapped_column(String(255), nullable=True, comment='描述')


class Feedback(BaseModel):
    """
    反馈表
    """
    __tablename__ = "ross_panel_feedback"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键')
    app_name = mapped_column(String(255), nullable=False, comment='app名称')
    text = mapped_column(String(255), nullable=False, comment='反馈内容')


class AppUpdate(BaseModel):
    """
    更新内容
    """
    __tablename__ = "ross_panel_app_update"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键')
    app_name = mapped_column(String(255), nullable=False, comment='app名称')
    version = mapped_column(String(255), nullable=False, comment='版本号')
    update_json = mapped_column(Text, nullable=False, comment='更新json')
    desc = mapped_column(String(255), nullable=True, comment='更新内容')
