# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:59
# @Author   : Ranshi
# @File     : stock.py
from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def user_root():
    return {'user': 'ranshi'}
