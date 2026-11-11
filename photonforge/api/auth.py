# -*- coding: utf-8 -*-
"""可选鉴权中间件。"""
from __future__ import annotations


def require_token(config):
    token = config.get("api.auth_token")
    if not token:
        return None

    def check(request):
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {token}":
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="unauthorized")
    return check
