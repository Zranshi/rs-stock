# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:50
# @Author   : Ranshi
# @File     : __init__.py
import datetime
from dataclasses import dataclass
from datetime import date

from sqlalchemy import Column, String, DateTime, Date, Float, BIGINT, create_engine
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

    def init_by_json(self, data):
        self.symbol = data['symbol']
        self.code = data['code']
        self.name = data['name']
        self.gmt_create = datetime.datetime.now()
        self.gmt_update = datetime.datetime.now()


@dataclass
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

    def init_by_json(self, data):
        self.code = data['code']
        self.day = date.today()
        self.start_price = data['open']
        self.end_price = data['settlement']
        self.low_price = data['low']
        self.high_price = data['high']
        self.volume = data['volume']
        self.volume_price = data['amount']
        self.change_rate = data['changepercent']
        self.gmt_create = datetime.datetime.now()
        self.gmt_update = datetime.datetime.now()


SQLALCHEMY_DATABASE_URL: str = f'mysql+pymysql://{Db.username}:{Db.password}@{Db.host}:' \
                               f'{Db.db_port}/{Db.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(bind=engine)()
