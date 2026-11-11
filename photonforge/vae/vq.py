# -*- coding: utf-8 -*-
"""VQ 码本量化：潜变量离散化到码本，压缩率高、利于缓存。"""
from __future__ import annotations

import math


def init_codebook(size: int, dim: int):
    """确定性初始化码本。"""
    codebook = []
    for i in range(size):
        entry = []
        for d in range(dim):
            entry.append(math.sin((i * dim + d) * 0.01))
        codebook.append(entry)
    return codebook


def nearest(codebook, vec):
    """最近邻检索（欧氏距离）。"""
    best = -1
    best_d = float("inf")
    for i, cb in enumerate(codebook):
        d = sum((a - b) ** 2 for a, b in zip(cb, vec))
        if d < best_d:
            best_d = d
            best = i
    return best


def quantize(codebook, vecs):
    """把向量序列量化成码本索引序列。"""
    return [nearest(codebook, v) for v in vecs]


def dequantize(codebook, indices):
    return [list(codebook[i]) for i in indices]
