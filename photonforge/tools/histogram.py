# -*- coding: utf-8 -*-
"""直方图与直方图均衡化。"""
from __future__ import annotations


def histogram(image, bins: int = 256):
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    hist = [0] * bins
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                b = min(bins - 1, int(image[cc][y][x] * bins))
                hist[b] += 1
    return hist


def equalize(image, bins: int = 256):
    hist = histogram(image, bins)
    cdf = []
    acc = 0
    total = sum(hist)
    for v in hist:
        acc += v
        cdf.append(acc / max(total, 1))
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    out = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(c)]
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                b = min(bins - 1, int(image[cc][y][x] * bins))
                out[cc][y][x] = cdf[b]
    return out
