# -*- coding: utf-8 -*-
"""图像格式转换。"""
from __future__ import annotations


def to_rgb(image):
    c = len(image)
    if c == 3:
        return image
    h = len(image[0])
    w = len(image[0][0])
    if c == 1:
        return [image[0], image[0], image[0]]
    return [image[i % c] for i in range(3)]


def to_grayscale(image):
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    return [[[sum(image[cc][y][x] for cc in range(c)) / c for x in range(w)] for y in range(h)]]
