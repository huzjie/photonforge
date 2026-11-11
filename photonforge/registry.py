# -*- coding: utf-8 -*-
"""组件注册中心：provider / sampler / 子系统的统一注册与查找。"""
from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self, name: str):
        self.name = name
        self._items: dict[str, T] = {}

    def register(self, key: str, obj: T = None):
        """既支持 @register("key") 装饰器，也支持 register("key", obj)。"""
        if obj is not None:
            self._items[key] = obj
            return obj

        def decorator(o: T) -> T:
            self._items[key] = o
            return o

        return decorator

    def get(self, key: str) -> T:
        if key not in self._items:
            raise KeyError(f"未知的 {self.name} 注册项: {key!r}（可用: {sorted(self._items)}）")
        return self._items[key]

    def keys(self) -> list[str]:
        return sorted(self._items)

    def __contains__(self, key: str) -> bool:
        return key in self._items


providers: Registry[Any] = Registry("provider")
samplers: Registry[Any] = Registry("sampler")
encoders: Registry[Any] = Registry("encoder")
