# -*- coding: utf-8 -*-
"""通用工具：确定性 RNG、进度、时间、格式化。"""
from __future__ import annotations

import hashlib
import random
import time


def seed_from(key: str) -> int:
    """从字符串键派生确定性种子（md5 前 8 字节），保证逐位可复现。"""
    digest = hashlib.md5(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def rng(key: str) -> random.Random:
    return random.Random(seed_from(key))


class Timer:
    def __init__(self):
        self._t0 = time.perf_counter()

    def elapsed(self) -> float:
        return time.perf_counter() - self._t0


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f}{unit}" if unit != "B" else f"{n}{unit}"
        n /= 1024
    return f"{n}B"
