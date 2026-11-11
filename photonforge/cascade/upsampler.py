# -*- coding: utf-8 -*-
"""潜空间上采样：低分辨率潜变量 -> 高分辨率潜变量。"""
from __future__ import annotations

from .. import vae


def upsample_latent(lat, scale: int):
    """潜空间双线性上采样（最近邻 + 均值平滑）。"""
    return vae.resize.nearest_neighbor(lat, scale)


def upscale_to_4k(low_lat, target: int = 4096, latent_scale: int = 8):
    """把低分辨率潜空间放大到 4K 目标潜空间。"""
    c = len(low_lat)
    h = len(low_lat[0])
    w = len(low_lat[0][0])
    th = target // latent_scale
    tw = target // latent_scale
    # 计算需要的放大倍数（至少 1）
    factor = max(th // h, tw // w, 1)
    up = low_lat
    while len(up[0]) < th and len(up[0][0]) < tw:
        up = upsample_latent(up, 2)
    # 裁到目标尺寸
    out = vae.latent.zeros(c, th, tw)
    for cc in range(c):
        for y in range(th):
            for x in range(tw):
                out[cc][y][x] = up[cc][min(y, len(up[0]) - 1)][min(x, len(up[0][0]) - 1)]
    return out
