# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:50
# @Author   : Ranshi
# @File     : __init__.py.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DB

SQLALCHEMY_DATABASE_URL: str = f'mysql+pymysql://{DB["username"]}:{DB["password"]}@{DB["ip"]}' \
                               f':3306/{DB["db_name"]}?charset=utf8'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
