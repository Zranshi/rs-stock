# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:50
# @Author   : Ranshi
# @File     : __init__.py
from dataclasses import dataclass

from sqlalchemy import Column, String, DateTime, Date, Float, BIGINT, create_engine, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Db

Base = declarative_base()


@dataclass
class Symbol(Base):
    __tablename__ = 'symbol'
    code = Column(String(16), primary_key=True)
    symbol = Column(String(32))
    name = Column(String(32))
    gmt_create = Column(DateTime)
    gmt_update = Column(DateTime)


@dataclass
class SymbolDay(Base):
    __tablename__ = 'symbol_day'
    code = Column(String(16))
    day = Column(Date)
    start_price = Column(Float)
    end_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(BIGINT)
    change_rate = Column(Float)
    volume_price = Column(Float)
    gmt_create = Column(DateTime)
    gmt_update = Column(DateTime)
    __table_args__ = (
        PrimaryKeyConstraint('code', 'day')
    )


SQLALCHEMY_DATABASE_URL: str = f'mysql+pymysql://{Db.username}:{Db.password}@{Db.host}:' \
                               f'{Db.db_port}/{Db.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(bind=engine)()
