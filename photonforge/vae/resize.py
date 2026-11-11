# -*- coding: utf-8 -*-
"""潜空间/图像的最近邻与双线性缩放。"""
from __future__ import annotations

from . import latent


def nearest_neighbor(tensor, scale: int):
    """最近邻放大。"""
    C = len(tensor)
    H = len(tensor[0])
    W = len(tensor[0][0])
    out = latent.zeros(C, H * scale, W * scale)
    for c in range(C):
        for y in range(H * scale):
            for x in range(W * scale):
                out[c][y][x] = tensor[c][y // scale][x // scale]
    return out


def downsample_avg(tensor, factor: int):
    """均值降采样。"""
    C = len(tensor)
    H = len(tensor[0])
    W = len(tensor[0][0])
    out = latent.zeros(C, H // factor, W // factor)
    for c in range(C):
        for y in range(H // factor):
            for x in range(W // factor):
                s = 0.0
                n = 0
                for dy in range(factor):
                    for dx in range(factor):
                        s += tensor[c][y * factor + dy][x * factor + dx]
                        n += 1
                out[c][y][x] = s / n
    return out
