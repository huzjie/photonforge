# -*- coding: utf-8 -*-
"""4K 分块解码：显存受限时把 4K 潜空间分块解码再拼接。"""
from __future__ import annotations

from .. import vae


def tiled_decode(lat, tile_size: int = 256, scale: int = 8, channels: int = 3):
    """分块解码，避免一次性分配 4K 图像内存。"""
    lh = len(lat[0])
    lw = len(lat[0][0])
    out = vae.latent.zeros(channels, lh * scale, lw * scale)
    for ly in range(0, lh, tile_size):
        for lx in range(0, lw, tile_size):
            sub = vae.latent.zeros(len(lat), tile_size, tile_size)
            for c in range(len(lat)):
                for y in range(tile_size):
                    for x in range(tile_size):
                        sy = min(ly + y, lh - 1)
                        sx = min(lx + x, lw - 1)
                        sub[c][y][x] = lat[c][sy][sx]
            decoded = vae.decoder.decode(sub, scale, channels)
            for c in range(channels):
                for y in range(tile_size * scale):
                    for x in range(tile_size * scale):
                        oy = ly * scale + y
                        ox = lx * scale + x
                        if oy < len(out[0]) and ox < len(out[0][0]):
                            out[c][oy][ox] = decoded[c][y][x]
    return out
