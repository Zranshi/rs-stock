# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:04
# @Author   : Ranshi
# @File     : main.py
import uvicorn

from app import get_app, APP

app = get_app()

if __name__ == '__main__':
    uvicorn.run(app, host=APP['host'], port=APP['port'])
