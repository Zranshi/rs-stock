# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:50
# @Author   : Ranshi
# @File     : __init__.py.py
from fastapi import APIRouter

from .stock import router as router_stock

router = APIRouter()

router.include_router(router_stock, tags=['stock'], prefix='/stock')
