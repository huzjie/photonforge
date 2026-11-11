# -*- coding: utf-8 -*-
"""蒙版工具。"""
from __future__ import annotations


def from_points(height, width, points, radius: int = 4):
    """从点集生成蒙版（每点画一个半径 radius 的圆）。"""
    m = [[0.0 for _ in range(width)] for _ in range(height)]
    for (cy, cx) in points:
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                y = cy + dy
                x = cx + dx
                if 0 <= y < height and 0 <= x < width and dx * dx + dy * dy <= radius * radius:
                    m[y][x] = 1.0
    return m


def blur(mask, radius: int = 8):
    """盒式模糊蒙版（羽化边缘）。"""
    if radius <= 0:
        return mask
    h = len(mask)
    w = len(mask[0])
    out = [[0.0 for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            s = 0.0
            n = 0
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    yy = y + dy
                    xx = x + dx
                    if 0 <= yy < h and 0 <= xx < w:
                        s += mask[yy][xx]
                        n += 1
            out[y][x] = s / n
    return out


def invert(mask):
    return [[1.0 - v for v in row] for row in mask]
