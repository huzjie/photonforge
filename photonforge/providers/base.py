# -*- coding: utf-8 -*-
"""Provider 基类与工厂。"""
from __future__ import annotations

from ..registry import providers


class BaseProvider:
    name = "base"

    def __init__(self, config=None):
        from ..config import Config
        self.config = config or Config.load()

    def generate(self, prompt, **kwargs):
        raise NotImplementedError

    def edit(self, instruction, image, **kwargs):
        raise NotImplementedError


def get_provider(name: str, config=None):
    """按名字获取 provider 实例。"""
    if name not in providers:
        raise KeyError(f"未知 provider: {name!r}（可用 {providers.keys()}）")
    cls = providers.get(name)
    return cls(config)
