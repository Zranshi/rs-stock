# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:59
# @Author   : Ranshi
# @File     : stock.py

import requests
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import HEADER
from app.models import Symbol, SymbolDay, session

templates = Jinja2Templates(directory="templates")

router = APIRouter()


def catch_symbol(page: int):
    stock_api_url = f'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData' \
                    f'?page={page}&num=100&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page'
    res = requests.get(url=stock_api_url, headers=HEADER).json()
    if len(res) == 0:
        return
    for item in res:
        s = Symbol()
        s.init_by_json(item)
        session.add(s)
    catch_symbol(page + 1)
    return


def catch_symbol_day(page: int):
    stock_api_url = f'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData' \
                    f'?page={page}&num=100&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page'
    res = requests.get(url=stock_api_url, headers=HEADER).json()
    if len(res) == 0:
        return
    for item in res:
        sd = SymbolDay()
        sd.init_by_json(item)
        print(sd.code, sd.end_price)
        session.add(sd)
    catch_symbol_day(page + 1)
    return


@router.get('/catch_today_data')
async def catch_data():
    """
    获取当前日期的股票信息，保存至数据库
    :return:
    """
    catch_symbol_day(1)
    session.commit()
    return {'msg': 'success'}


@router.get('/stock_table')
async def show(request: Request):
    """
    返回数据页面
    :param request:
    :return:
    """
    return templates.TemplateResponse("stock_table.html", {
        "request": request,
        "stock_data": session.query(SymbolDay).all(),
    }, )
