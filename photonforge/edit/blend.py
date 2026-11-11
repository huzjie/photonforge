# -*- coding: utf-8 -*-
"""图像/潜变量混合。"""
from __future__ import annotations


def feather_blend(base, edit, mask):
    """按蒙版羽化混合：out = base*(1-mask) + edit*mask。"""
    c = len(base)
    h = len(base[0])
    w = len(base[0][0])
    out = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(c)]
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                a = mask[y][x]
                out[cc][y][x] = base[cc][y][x] * (1 - a) + edit[cc][y][x] * a
    return out


def alpha_blend(base, edit, alpha: float):
    c = len(base)
    h = len(base[0])
    w = len(base[0][0])
    out = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(c)]
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                out[cc][y][x] = base[cc][y][x] * (1 - alpha) + edit[cc][y][x] * alpha
    return out
