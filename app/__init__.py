# -*- coding:utf-8 -*-
# @Time     : 2021/6/9 21:42
# @Author   : Ranshi
# @File     : __init__.py
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse

from .apis import router
from .config import App
from .models import session


def get_app() -> FastAPI:
    """
    设置好项目的app，并放回fastAPI实例
    :return:
    """
    app = FastAPI()

    origins = {
        "http://localhost",
        "http://localhost:8080",
    }
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=500,
    )

    @app.middleware('http')
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    app.include_router(router, prefix='/apis')  # 配置路由

    @app.get('/')
    async def init():
        """
        根路由跳转到/apis/stock/all
        :return:
        """
        return RedirectResponse('/apis/stock/all')

    @app.on_event("shutdown")
    async def shutdown():
        await session.close_all()

    return app
