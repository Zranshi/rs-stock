# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:50
# @Author   : Ranshi
# @File     : __init__.py.py
from sqlalchemy import Column, String, DateTime, Date, Float, BIGINT, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DB

Base = declarative_base()


class Symbol(Base):
    __tablename__ = 'symbol'

    code = Column(String(16), primary_key=True)
    symbol = Column(String(32))
    name = Column(String(32))
    gmt_create = Column(DateTime)
    gmt_update = Column(DateTime)


class SymbolDay(Base):
    __tablename__ = 'symbol_day'
    code = Column(String(16), primary_key=True)
    day = Column(Date, primary_key=True)
    start_price = Column(Float)
    end_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(BIGINT)
    change_rate = Column(Float)
    volume_price = Column(Float)
    gmt_create = Column(DateTime)
    gmt_update = Column(DateTime)


SQLALCHEMY_DATABASE_URL: str = f'mysql+pymysql://{DB["username"]}:{DB["password"]}@{DB["ip"]}:' \
                               f'{DB["db_port"]}/{DB["db_name"]}?charset=utf8'

database = create_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(bind=database)
