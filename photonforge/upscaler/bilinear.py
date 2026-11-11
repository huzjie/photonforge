# -*- coding: utf-8 -*-
"""双线性插值上采样。"""
from __future__ import annotations


def upscale(image, factor: int = 2):
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    nh = h * factor
    nw = w * factor
    out = [[[0.0 for _ in range(nw)] for _ in range(nh)] for _ in range(c)]
    for cc in range(c):
        for y in range(nh):
            for x in range(nw):
                sy = y / factor
                sx = x / factor
                y0 = int(sy)
                x0 = int(sx)
                y1 = min(y0 + 1, h - 1)
                x1 = min(x0 + 1, w - 1)
                fy = sy - y0
                fx = sx - x0
                top = image[cc][y0][x0] * (1 - fx) + image[cc][y0][x1] * fx
                bot = image[cc][y1][x0] * (1 - fx) + image[cc][y1][x1] * fx
                out[cc][y][x] = top * (1 - fy) + bot * fy
    return out
