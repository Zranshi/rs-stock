# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:59
# @Author   : Ranshi
# @File     : stock.py

from datetime import date, timedelta

import requests
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, desc
from app.config import HEADER
from app.models import Symbol, SymbolDay, session

templates = Jinja2Templates(directory="templates/stock")
router = APIRouter()
now = date.today() - timedelta(1)


def catch_symbol(page: int):
    """
    爬取symbol表数据，并保存到数据库
    :param page: api 页面参数
    :return:
    """
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
    """
    爬取当天的symbol_day表数据，并保存到数据库
    :param page: api 页面参数
    :return:
    """
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
    """
    爬取当天的symbol_day表数据，并保存到数据库
    :return: 返回是否成功
    """
    catch_symbol_day(1)
    session.commit()
    return {
        'msg': 'success'
    }


@router.get('/data')
async def chart_data(code: str):
    """
    获取chart数据，
    :param code: 股票code
    :return: 返回图表数据，数据为json格式
    """
    res = session.query(SymbolDay) \
        .filter(SymbolDay.code == code) \
        .order_by(SymbolDay.day) \
        .all()
    data, time = [], []
    for item in res:
        data.append([item.start_price, item.end_price, item.low_price, item.high_price])
        time.append(item.day)
    return {
        'data': data,
        'time': time
    }


@router.get('/search')
async def search_html(re: Request, up: bool, per: float, day: int):
    """
    按照day天内上升/下降量搜索数据
    :param re:
    :param up: 是否上升
    :param per: 比例数据
    :param day: 天数
    :return: 返回搜索页面
    """
    pre = session.query(SymbolDay) \
        .filter(SymbolDay.day == now - timedelta(day)) \
        .all()
    data_now = session.query(SymbolDay) \
        .filter(SymbolDay.day == now) \
        .all()
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
    return templates.TemplateResponse('search.html', {
        'request': re,
        'data': data,
    })


@router.get('/all')
async def stock_all_html(re: Request):
    """
    获取所有的symbol数据
    :param re:
    :return: 返回所有symbol页面
    """
    return templates.TemplateResponse('all_stock.html', {
        'request': re,
        'data': session.query(Symbol).all(),
    })


@router.get('/info')
async def stock_info_html(re: Request, code: int):
    """
    获取股票详情
    :param re:
    :param code: 股票code
    :return: 返回详情页面
    """
    data = session.query(Symbol) \
        .filter(Symbol.code == code) \
        .first()
    x = session.query(SymbolDay.end_price, SymbolDay.day) \
        .filter(and_(SymbolDay.day == now, SymbolDay.code == code)) \
        .first()
    y = session.query(SymbolDay.end_price, SymbolDay.day) \
        .filter(and_(SymbolDay.day < now, SymbolDay.code == code)) \
        .order_by(desc(SymbolDay.day)) \
        .first()
    rate = ((((x.end_price - y.end_price) / y.end_price) / (x.day - y.day).days) * 100)
    rate = round(rate, 2)
    return templates.TemplateResponse('stock_info.html', {
        'request': re,
        'data': data,
        'rate': rate,
    })
