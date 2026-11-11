# -*- coding: utf-8 -*-
"""图像元数据：尺寸、通道、统计。"""
from __future__ import annotations


def shape(image):
    return (len(image), len(image[0]), len(image[0][0]))


def stats(image):
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    n = c * h * w
    flat = [image[cc][y][x] for cc in range(c) for y in range(h) for x in range(w)]
    mean = sum(flat) / n
    var = sum((v - mean) ** 2 for v in flat) / n
    return {"channels": c, "height": h, "width": w, "mean": mean, "var": var}
