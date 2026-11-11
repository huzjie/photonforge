# -*- coding: utf-8 -*-
"""请求/响应模型。"""
from __future__ import annotations

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    def Field(default=None, **kw):  # type: ignore
        return default


class GenerateRequest(BaseModel):
    prompt: str
    reference_images: list = Field(default_factory=list)
    ref_weights: list = Field(default_factory=list)
    steps: int = 12
    guidance: float = 4.5
    width: int = 1024
    height: int = 1024


class EditRequest(BaseModel):
    instruction: str
    image: list = Field(default_factory=list)
    strength: float = 0.75


class GenerateResponse(BaseModel):
    status: str = "ok"
    image: list = Field(default_factory=list)
    elapsed: float = 0.0
