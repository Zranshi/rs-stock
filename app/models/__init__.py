# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:50
# @Author   : Ranshi
# @File     : __init__.py.py
from databases import Database

from app.config import DB

SQLALCHEMY_DATABASE_URL: str = f'mysql://{DB["username"]}:{DB["password"]}@{DB["ip"]}:' \
                               f'{DB["db_port"]}/{DB["db_name"]}?charset=utf8'

database = Database(SQLALCHEMY_DATABASE_URL)
