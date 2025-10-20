from sqlalchemy import String, Integer, DateTime, Computed, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from db.db_base import BaseModel



class RossQuestionTemplate(BaseModel):
    __tablename__ = "ross_question_template"
    __table_args__ = ({'comment': '问题模板表'})

    title = mapped_column(String(125), nullable=False, default="", comment="标题")
    description = mapped_column(String(2048), nullable=False, default="", comment="描述")
    status = mapped_column(Integer, nullable=False, default=1, comment="状态")
    sale_agent_id = mapped_column(Integer, nullable=False, default=0, comment="售前代理ID")


class RossQuestion(BaseModel):
    __tablename__ = "ross_question"
    __table_args__ = ({'comment': '问题表'})
    template_id = mapped_column(Integer, nullable=False, comment="模板ID")
    question = mapped_column(String(2048), nullable=False, default="", comment="问题")


class RossAnswer(BaseModel):
    __tablename__ = "ross_answer"
    __table_args__ = ({'comment': '回答表'})
    question_id = mapped_column(Integer, nullable=False, comment="问题ID")
    next_question = mapped_column(Integer, nullable=True, comment="下一题")
    answer = mapped_column(String(255), nullable=False, default="", comment="答案")
    customer_tag = mapped_column(String(50), nullable=True, default="", comment="客户标签,回答了这个问题代表该客户是这个标签的群体")





