from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from db.db_base import BaseModel


class FbMessage(BaseModel):
    """
      Facebook Messenger 消息表
      存储通过 Webhook 接收到或发送的消息内容。
      """
    __tablename__ = "fb_message"
    __table_args__ = {"comment": "facebook message"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")

    message_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="Facebook 消息ID")
    type: Mapped[str] = mapped_column(String(20), nullable=False, comment="消息类型，如 text/image/postback 等")
    content: Mapped[str] = mapped_column(String(1024), nullable=False, comment="消息内容")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="received",
                                        comment="消息状态，如 received/sent/read 等")
    meta_data: Mapped[str] = mapped_column(String(1024), nullable=True, comment="消息元数据（如附件、按钮参数等）")

    sender_id: Mapped[str] = mapped_column(String(100), nullable=False, comment="发送者ID（用户PSID）")
    recipient_id: Mapped[str] = mapped_column(String(100), nullable=False, comment="接收者ID（页面ID）")

