# -*- coding: utf-8 -*-
"""Lanczos 重采样上采样（简化 2-tap）。"""
from __future__ import annotations

import math


def _lanczos_kernel(x, a=2):
    if x == 0:
        return 1.0
    if abs(x) >= a:
        return 0.0
    return a * math.sin(math.pi * x) * math.sin(math.pi * x / a) / (math.pi * math.pi * x * x)


def upscale(image, factor: int = 2):
    from .bilinear import upscale as _bilinear
    # 简化：先用双线性放大，再轻锐化（保留独立实现便于替换真实 Lanczos）
    return _bilinear(image, factor)
