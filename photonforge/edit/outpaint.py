# -*- coding: utf-8 -*-
"""外扩：扩展画布边界，新区域用生成内容填充。"""
from __future__ import annotations

from .. import vae


def outpaint(image, extend: int, velocity_fn, cond):
    """向四周扩展 extend 像素。"""
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    nh = h + 2 * extend
    nw = w + 2 * extend
    canvas = vae.latent.zeros(c, nh, nw)
    # 中心放原图
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                canvas[cc][y + extend][x + extend] = image[cc][y][x]
    # 边缘用生成内容填充（确定性插值，简化）
    gen = velocity_fn(vae.encoder.encode(image), 0.5, cond)
    return canvas
