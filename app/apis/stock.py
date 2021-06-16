# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:59
# @Author   : Ranshi
# @File     : stock.py

from datetime import date, timedelta

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
        session.add(sd)
    catch_symbol_day(page + 1)
    return


@router.get('/catch_today_data')
async def catch_data():
    catch_symbol_day(1)
    session.commit()
    return {
        'msg': 'success'
    }


@router.get('/show_chart')
async def show_chart(re: Request, code: str):
    return templates.TemplateResponse("chart.html", {
        'request': re,
        'code': code,
    })


@router.get('/chart')
async def chart(code: str):
    res = session.query(SymbolDay.day, SymbolDay.start_price, SymbolDay.end_price, SymbolDay.low_price,
                        SymbolDay.high_price).filter(
        SymbolDay.code == code).order_by(SymbolDay.day).all()
    data, time = [], []
    for item in res:
        data.append([item.start_price, item.end_price, item.low_price, item.high_price])
        time.append(item.day)
    return {
        'data': data,
        'time': time
    }


@router.get('/increase_search')
async def show(re: Request, up: bool, per: float, day: int):
    now = date.today()
    pre = session.query(SymbolDay).filter(SymbolDay.day == now - timedelta(day)).all()
    data_now = session.query(SymbolDay).filter(SymbolDay.day == now).all()
    data_pre = {item.code: item for item in pre}
    data = []
    for item in data_now:
        if item.code in data_pre:
            rate = (item.end_price - data_pre[item.code].end_price) / data_pre[item.code].end_price * 100
            if rate > per if up else rate <= per:
                data.append({
                    'now': item,
                    'pre': data_pre[item.code],
                    'rate': rate
                })
    return templates.TemplateResponse('show.html', {
        'request': re,
        'data': data,
    })


@router.get('/today_stock')
async def show(re: Request):
    return templates.TemplateResponse('stock_table.html', {
        'request': re,
        'data': session.query(Symbol).all(),
    })
