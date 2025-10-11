from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column

from db.db_base import BaseModel


class RossFiles(BaseModel):
    """
    文件管理系统
    用于存储和管理所有上传的文件信息
    """
    __tablename__ = "ross_files"
    __table_args__ = (
        {'comment': '文件存储表'},
    )

    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment="文件ID")
    filename = mapped_column(String(255), nullable=False, comment="原始文件名称")
    storage_name = mapped_column(String(255), nullable=False, unique=True, comment="存储文件名称")
    file_path = mapped_column(String(500), nullable=False, comment="文件存储路径")
    file_url = mapped_column(String(500), nullable=False, comment="文件访问URL")
    md5 = mapped_column(String(32), nullable=False, index=True, comment="文件MD5哈希值")
    file_size = mapped_column(Integer, nullable=False, comment="文件大小(MB)")
    file_type = mapped_column(String(100), nullable=False, comment="文件MIME类型")
    file_extension = mapped_column(String(50), nullable=False, comment="文件扩展名")

    # 关联信息
    uploader_id = mapped_column(Integer, nullable=True, comment="上传用户ID")
    app_name = mapped_column(String(100), nullable=True, comment="关联应用名称")
    category = mapped_column(String(100), nullable=True, comment="文件分类")

    # 状态管理
    status = mapped_column(String(20), default='active', comment="文件状态: active/inactive/deleted")
    is_public = mapped_column(Boolean, default=False, comment="是否公开访问")