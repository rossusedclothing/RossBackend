from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column

from db.db_base import BaseModel


class SalesAgentConfig(BaseModel):
    __tablename__ = "ross_sales_agent"
    __table_args__ = ({'comment': '业务员配置'})

    phone = mapped_column(String(20), nullable=False, comment='手机号 and sales_agent_id ', unique=True)
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
    customer_phone = mapped_column(String(20), nullable=True, comment='客户手机号', index=True, unique=True)
    customer_name = mapped_column(String(50), nullable=True, comment='客户名称', index=True)
    platform = mapped_column(String(20), default='whatsapp', nullable=True, comment='平台')
    meta_data = mapped_column(Text, nullable=True, comment='元数据')
    tag = mapped_column(String(20), default='standard_consumer', nullable=True,
                        comment='用户标签 取值：full_consumer,standard_consumer,small_consumer,agents_consumer,supplier_consumer	')
    is_tag_changed = mapped_column(Integer, default=0, nullable=True, comment='是否修改标签: 0-否 1-是')
    summary_content = mapped_column(Text, nullable=True, comment='近期聊天总结')


class ReBotCustomerMessage(BaseModel):
    __tablename__ = "ross_customer_history"
    __table_args__ = ({'comment': '历史消息表'})
    customer_phone = mapped_column(String(20), nullable=True, comment='客户手机号')
    customer_name = mapped_column(String(20), nullable=True, comment='客户名称', index=True)
    customer_message = mapped_column(Text, nullable=True, comment='客户消息')
    receiver_message = mapped_column(Text, default="", nullable=True, comment='回复消息')
