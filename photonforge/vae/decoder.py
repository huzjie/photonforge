# -*- coding: utf-8 -*-
"""VAE 解码器：潜空间 -> 图像（8x 上采样）。"""
from __future__ import annotations

from . import latent


def decode(lat, scale: int = 8, channels: int = 3):
    """确定性解码：潜变量最近邻上采样回像素空间。"""
    lc = len(lat)
    lh = len(lat[0])
    lw = len(lat[0][0])
    out = latent.zeros(channels, lh * scale, lw * scale)
    for ly in range(lh):
        for lx in range(lw):
            base = []
            for c in range(channels):
                base.append(lat[c % lc][ly][lx])
            for y in range(scale):
                for x in range(scale):
                    for c in range(channels):
                        out[c][ly * scale + y][lx * scale + x] = base[c]
    return out
