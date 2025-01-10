from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Text, JSON, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from datetime import datetime

BaseEntity = declarative_base()


class MvManage(BaseEntity):
    __tablename__ = 'mv_manage_latest'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键')
    blurb = Column(String(1000), nullable=True, comment='简介信息')
    picture = Column(String(1000), nullable=True, comment='封面图片')
    address = Column(Text, nullable=True, comment='资源地址')
    area = Column(String(50), nullable=False, comment='区域')
    class_tag = Column(JSON, nullable=False, comment='标签')
    state = Column(TINYINT, nullable=False, default=1, comment='数据状态0=无效；1=有效；')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
