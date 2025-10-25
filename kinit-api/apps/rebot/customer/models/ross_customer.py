from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column

from db.db_base import BaseModel


class SalesAgentConfig(BaseModel):
    __tablename__ = "ross_sales_agent"
    __table_args__ = ({'comment': '业务员配置'})

    phone = mapped_column(String(20), nullable=False, comment='手机号 and sales_agent_id ',unique= True)
    name = mapped_column(String(50), nullable=False, comment='名称')
    description = mapped_column(Text, comment='描述')
    config = mapped_column(Text, comment='配置')


class SalesAgentWorkflow(BaseModel):
    __tablename__ = "ross_sales_agentWork_flow"
    __table_args__ = ({'comment': '业务员工作流'})

    phone = mapped_column(String(20), comment='手机号')
    name = mapped_column(String(20), comment='名称')
    description = mapped_column(Text, comment='描述')
    config = mapped_column(Text, comment='配置信息')


class ReBotCustomer(BaseModel):
    __tablename__ = "ross_customer"
    __table_args__ = ({'comment': '客户表'})

    sales_agent_id = mapped_column(String(20), default=1, nullable=True, comment='所属业务员')
    customer_phone = mapped_column(String(125), nullable=True, comment='客户手机号', index=True,unique= True)
    customer_name = mapped_column(String(125), nullable=True, comment='客户名称', index=True)
    platform = mapped_column(String(20), default='whatsapp', nullable=True, comment='平台')
    meta_data = mapped_column(Text, nullable=True, comment='元数据')
    user_tag = mapped_column(String(50), nullable=True, comment='用户标签')
    summary_content = mapped_column(Text, nullable=True, comment='摘要内容')
    sales_repp_phone = mapped_column(String(20), nullable=True, comment='销售代表手机号')
    sales_agent_phone = mapped_column(String(20), nullable=True, comment='业务员手机号')
    is_tagged = mapped_column(Integer, default=0, nullable=True, comment='是否打标签 0 未打标签 1 已打标签')
    answering_progress = mapped_column(Integer, default=1, nullable=True, comment='问题进度')

class ReBotCustomerMessage(BaseModel):
    __tablename__ = "ross_customer_history"
    __table_args__ = ({'comment': '历史消息表'})
    customer_phone = mapped_column(String(20), nullable=True, comment='客户手机号')
    customer_name = mapped_column(String(20), nullable=True, comment='客户名称', index=True)
    customer_message = mapped_column(Text, nullable=True, comment='客户消息')
    receiver_message = mapped_column(Text, default="", nullable=True, comment='回复消息')
