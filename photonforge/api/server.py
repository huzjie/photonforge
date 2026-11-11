# -*- coding: utf-8 -*-
"""FastAPI 服务器：生成 / 编辑 / 健康检查。"""
from __future__ import annotations


def create_app():
    from fastapi import FastAPI
    from .routes import router

    app = FastAPI(title="photonforge", version="0.1.0",
                  description="高速多参考图图像生成与编辑引擎")
    app.include_router(router)
    return app


def run(host="127.0.0.1", port=8000):
    import uvicorn
    uvicorn.run(create_app(), host=host, port=port)
