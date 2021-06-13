# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:59
# @Author   : Ranshi
# @File     : stock.py
import datetime
from datetime import date

import requests
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import HEADER
from app.models import Symbol, SymbolDay, session

templates = Jinja2Templates(directory="templates")

router = APIRouter()


def catch(page: int):
    stock_api_url = f'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData' \
                    f'?page={page}&num=100&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page'
    res = requests.get(url=stock_api_url, headers=HEADER).json()
    for item in res:
        s = Symbol(
            symbol=item['symbol'],
            code=item['code'],
            name=item['name'],
            gmt_create=datetime.datetime.now(),
            gmt_update=datetime.datetime.now(),
        )
        sd = SymbolDay(
            code=item['code'],
            day=date.today(),
            start_price=item['open'],
            end_price=item['settlement'],
            low_price=item['low'],
            high_price=item['high'],
            volume=item['volume'],
            volume_price=item['amount'],
            change_rate=item['changepercent'],
            gmt_create=datetime.datetime.now(),
            gmt_update=datetime.datetime.now(),
        )
        session.add(s)
        session.add(sd)
    session.commit()


@router.get('/catch_today_data')
async def catch_data():
    """
    获取当前日期的股票信息，保存至数据库
    :return:
    """
    for i in range(1, 45):
        catch(i)
    return {'success': True}


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
