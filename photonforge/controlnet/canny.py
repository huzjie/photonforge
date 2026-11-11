# -*- coding: utf-8 -*-
"""Canny 边缘检测（纯标准库简化实现）。"""
from __future__ import annotations


def grayscale(image):
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    return [[sum(image[cc][y][x] for cc in range(c)) / c for x in range(w)] for y in range(h)]


def sobel_edges(gray):
    h = len(gray)
    w = len(gray[0])
    out = [[0.0 for _ in range(w)] for _ in range(h)]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            gx = (gray[y-1][x+1] + 2*gray[y][x+1] + gray[y+1][x+1]) - \
                 (gray[y-1][x-1] + 2*gray[y][x-1] + gray[y+1][x-1])
            gy = (gray[y+1][x-1] + 2*gray[y+1][x] + gray[y+1][x+1]) - \
                 (gray[y-1][x-1] + 2*gray[y-1][x] + gray[y-1][x+1])
            out[y][x] = (gx * gx + gy * gy) ** 0.5
    return out


def extract(image):
    return sobel_edges(grayscale(image))
