from sqlalchemy import String, Integer, DateTime, Computed, func, text
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from db.db_base import BaseModel


class RossActivationCodes(BaseModel):
    """激活码模型"""
    __tablename__ = "ross_activation_codes"

    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键')
    code = mapped_column(String(64), nullable=False, unique=True, comment='激活码')
    type = mapped_column(String(20), nullable=False, default='trial',
                         comment='类型：trial-试用, personal-个人, team-团队, enterprise-企业')
    status = mapped_column(String(20), nullable=False, default='active',
                           comment='状态：active-未使用, used-已使用, expired-已过期, revoked-已撤销')
    user_limit = mapped_column(Integer, nullable=False, default=1, comment='用户数量限制')
    duration_days = mapped_column(Integer, nullable=False, default=30, comment='有效期天数')
    features = mapped_column(String(1024), comment='功能权限配置')
    created_by = mapped_column(String(100), comment='创建者')
    activated_by = mapped_column(String(100), comment='激活者')
    activated_datetime = mapped_column(DateTime, comment='激活时间')
    expires_datetime = mapped_column(
        DateTime,
        nullable=True,
        comment='过期时间'
    )
    # create_datetime = mapped_column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    # update_datetime = mapped_column(DateTime, nullable=False, server_default=func.now(), comment='更新时间')
    # delete_datetime = mapped_column(DateTime, nullable=False, server_default=func.now(), comment='删除时间')
    # is_delete = mapped_column(Integer, nullable=False, default=0, comment='是否删除：0-否, 1-是')

class RossActivationRecords(Base):
    """激活记录模型"""
    __tablename__ = "ross_activation_records"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键')
    code_id = mapped_column(Integer, nullable=False, comment='激活码ID')
    user_id = mapped_column(String(100), nullable=False, comment='用户ID')
    device_id = mapped_column(String(100), comment='设备ID')
    device_info = mapped_column(String(1024), comment='设备信息')
    ip_address = mapped_column(String(45), comment='IP地址')
    activated_datetime = mapped_column(DateTime, nullable=False, server_default=func.now(), comment='激活时间')
    last_verified_datetime = mapped_column(DateTime, comment='最后验证时间')
    status = mapped_column(String(20), nullable=False, default='active',
                           comment='状态：active-有效, expired-过期, revoked-撤销')

    is_delete = mapped_column(Integer, nullable=False, default=0, comment='是否删除：0-否, 1-是')