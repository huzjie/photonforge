# -*- coding: utf-8 -*-
"""VAE 编码器：图像 -> 潜空间（8x 下采样）。"""
from __future__ import annotations

from . import latent


def encode(image, scale: int = 8, channels: int = 4):
    """确定性编码：对每个 scale*scale 像素块做均值 + 方差压缩到潜变量。

    image: [C][H][W] 的像素张量。
    返回: [channels][H//scale][W//scale] 潜空间张量。
    """
    C = len(image)
    H = len(image[0])
    W = len(image[0][0])
    lh = H // scale
    lw = W // scale
    out = latent.zeros(channels, lh, lw)
    for ly in range(lh):
        for lx in range(lw):
            block = []
            for y in range(ly * scale, ly * scale + scale):
                for x in range(lx * scale, lx * scale + scale):
                    block.append([image[c][y][x] for c in range(C)])
            n = len(block)
            # 通道均值与离散度作为潜变量（4 通道：mean_r, mean_g, mean_b, energy）
            for c in range(min(channels, C)):
                m = sum(b[c] for b in block) / n
                out[c][ly][lx] = m
            if channels > C:
                energy = sum(b[c % C] ** 2 for b in block for c in range(1)) / n
                out[C][ly][lx] = energy
    return out
