# -*- coding: utf-8 -*-
"""RoPE 旋转位置编码（纯标准库）。"""
from __future__ import annotations

import math


def apply_rope(x, pos: int, theta: float = 10000.0):
    """对单个 token 向量施加旋转位置编码。x: [dim]。"""
    dim = len(x)
    out = list(x)
    for i in range(0, dim - 1, 2):
        freq = theta ** (-2 * i / dim)
        angle = pos * freq
        c = math.cos(angle)
        s = math.sin(angle)
        x0 = x[i]
        x1 = x[i + 1]
        out[i] = x0 * c - x1 * s
        out[i + 1] = x0 * s + x1 * c
    return out


def apply_rope_sequence(seq, theta: float = 10000.0):
    return [apply_rope(tok, i, theta) for i, tok in enumerate(seq)]
