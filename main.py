# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:04
# @Author   : Ranshi
# @File     : main.py
import uvicorn

from app import get_app
from app.config import App

app = get_app()

if __name__ == '__main__':
    uvicorn.run(app='main:app', host=App.host, port=App.port, reload=True, debug=True)
