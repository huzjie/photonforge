# -*- coding: utf-8 -*-
"""图像 -> patch 序列：把潜空间图切成 patch 当 token，供 Transformer 处理。"""
from __future__ import annotations


def patchify(image, patch_size: int = 2):
    """把 2D 图像（潜空间张量）切成 patch 序列。

    image: list[list[list]] 形状 [C][H][W]
    返回: [num_patches][C * patch_size * patch_size] 的 token 序列，按行优先扫描。
    """
    C = len(image)
    H = len(image[0])
    W = len(image[0][0])
    ph = patch_size
    pw = patch_size
    tokens = []
    for y in range(0, H, ph):
        for x in range(0, W, pw):
            flat = []
            for c in range(C):
                for dy in range(ph):
                    for dx in range(pw):
                        yy = min(y + dy, H - 1)
                        xx = min(x + dx, W - 1)
                        flat.append(image[c][yy][xx])
            tokens.append(flat)
    return tokens


def unpatchify(tokens, channels: int, height: int, width: int, patch_size: int = 2):
    """patch 序列 -> 图像（patchify 的逆操作）。"""
    image = [[[0.0 for _ in range(width)] for _ in range(height)] for _ in range(channels)]
    ph = patch_size
    pw = patch_size
    idx = 0
    for y in range(0, height, ph):
        for x in range(0, width, pw):
            token = tokens[idx]
            k = 0
            for c in range(channels):
                for dy in range(ph):
                    for dx in range(pw):
                        yy = min(y + dy, height - 1)
                        xx = min(x + dx, width - 1)
                        image[c][yy][xx] = token[k]
                        k += 1
            idx += 1
    return image


def grid_size(height: int, width: int, patch_size: int = 2):
    """patch 网格尺寸。"""
    import math
    return math.ceil(height / patch_size), math.ceil(width / patch_size)
