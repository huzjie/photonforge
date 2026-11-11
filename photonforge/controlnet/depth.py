# -*- coding: utf-8 -*-
"""深度估计占位：接真实单目深度模型（如 MiDaS / Depth Anything）。"""
from __future__ import annotations


def estimate(image):
    """简化深度（用亮度近似距离）。"""
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    return [[sum(image[cc][y][x] for cc in range(c)) / c for x in range(w)] for y in range(h)]
