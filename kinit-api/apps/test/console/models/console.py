from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from db.db_base import BaseModel

# create table test_console
# (
#     id          bigint unsigned null,
#     name        varchar(255)    null,
#     description varchar(255)    null,
#     price       decimal(10, 2)  null,
#     created_at  timestamp       null,
#     updated_at  timestamp       null,
#     deleted_at  timestamp       null,
#     is_deleted  tinyint         null,
#     is_active   tinyint         null
# );

class Console(BaseModel):
    __tablename__ = "test_console"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255))
    description = mapped_column(String(255))
    price = mapped_column(String(255))
    is_active = mapped_column(Integer)


# 问题反馈
class Issue(BaseModel):
    __tablename__ = "test_issue"
    id = mapped_column(Integer, primary_key=True, autoincrement=True,doc="ID")
    title = mapped_column(String(255),nullable= True, default='',doc="标题")
    content = mapped_column(String(255),nullable= True, default='',doc="内容")
