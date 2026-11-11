# -*- coding: utf-8 -*-
"""Web 控制台静态页挂载。"""
from __future__ import annotations

import os

INDEX_HTML = os.path.join(os.path.dirname(__file__), "index.html")


def mount(app):
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    from fastapi.staticfiles import StaticFiles

    @app.get("/", response_class=HTMLResponse)
    def index():
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            return f.read()
