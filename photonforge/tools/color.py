# -*- coding: utf-8 -*-
"""颜色工具：亮度/对比度/饱和度调整。"""
from __future__ import annotations


def adjust_brightness(image, delta: float):
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    out = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(c)]
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                out[cc][y][x] = max(0.0, min(1.0, image[cc][y][x] + delta))
    return out


def adjust_contrast(image, factor: float):
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    mean = sum(image[cc][y][x] for cc in range(c) for y in range(h) for x in range(w)) / (c * h * w)
    out = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(c)]
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                out[cc][y][x] = max(0.0, min(1.0, (image[cc][y][x] - mean) * factor + mean))
    return out
