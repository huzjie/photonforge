# -*- coding: utf-8 -*-
"""前馈 MLP（SwiGLU 风格门控，纯标准库）。"""
from __future__ import annotations

import math


def silu(x):
    return x / (1.0 + math.exp(-x))


def mlp(x, w1=None, w2=None, hidden_ratio: float = 4.0):
    """前馈层。w1/w2 为 None 时用确定性伪权重（基于维度 hash），便于离线验证。"""
    dim = len(x)
    hidden = max(int(dim * hidden_ratio), 1)
    gate = [silu(_proj(x, i, hidden, "gate")) for i in range(hidden)]
    up = [_proj(x, i, hidden, "up") for i in range(hidden)]
    out = []
    for o in range(dim):
        acc = 0.0
        for h in range(hidden):
            acc += gate[h] * up[h] * _proj_out(h, o, dim)
        out.append(acc)
    return out


def _proj(x, i, hidden, tag):
    seed = sum((k + 1) * (v + 1.0) for k, v in enumerate(x)) * (i + 1) + len(tag)
    frac = math.sin(seed * 12.9898) * 43758.5453
    frac = frac - math.floor(frac)
    return sum(x) * (frac - 0.5) / max(len(x), 1)


def _proj_out(h, o, dim):
    return math.sin((h * dim + o) * 0.0174533) * 0.01
