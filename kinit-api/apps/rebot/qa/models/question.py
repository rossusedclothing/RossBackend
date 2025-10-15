from sqlalchemy import String, Integer, DateTime, Computed, func
from sqlalchemy.orm import Mapped, mapped_column

from db.db_base import BaseModel


class RossQuestion(BaseModel):
    __tablename__ = "ross_question"
    __table_args__ = ({'comment': '问题表'})
    question = mapped_column(String(2048), nullable=False, default="", comment="问题")


class RossAnswer(BaseModel):
    __tablename__ = "ross_answer"
    __table_args__ = ({'comment': '回答表'})
    question_id = mapped_column(Integer, nullable=False, comment="问题ID")
    next_question = mapped_column(Integer, nullable=True, comment="下一题")
    answer = mapped_column(String(255), nullable=False, default="", comment="答案")
