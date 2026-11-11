# -*- coding: utf-8 -*-
"""图像工具：缩放、裁剪、翻转、灰度。"""
from __future__ import annotations


def resize_nearest(image, height, width):
    from ..vae import latent
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    out = latent.zeros(c, height, width)
    for cc in range(c):
        for y in range(height):
            for x in range(width):
                out[cc][y][x] = image[cc][min(y * h // height, h - 1)][min(x * w // width, w - 1)]
    return out


def crop(image, top, left, height, width):
    from ..vae import latent
    c = len(image)
    out = latent.zeros(c, height, width)
    for cc in range(c):
        for y in range(height):
            for x in range(width):
                out[cc][y][x] = image[cc][top + y][left + x]
    return out


def flip_h(image):
    c = len(image)
    return [[row[::-1] for row in image[cc]] for cc in range(c)]


def flip_v(image):
    c = len(image)
    return [image[cc][::-1] for cc in range(c)]


def grayscale(image):
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    out = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(1)]
    for y in range(h):
        for x in range(w):
            s = sum(image[cc][y][x] for cc in range(c)) / c
            out[0][y][x] = s
    return out
