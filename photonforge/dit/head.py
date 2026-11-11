# -*- coding: utf-8 -*-
"""DiT 输出头：token 序列 -> patch 像素。"""
from __future__ import annotations


def final_layer(seq, patch_dim: int):
    """线性投影到 patch 像素空间。seq: [num_patches][dim]。"""
    out = []
    for tok in seq:
        patch = []
        for i in range(patch_dim):
            v = sum(tok) / max(len(tok), 1)
            patch.append(v)
        out.append(patch)
    return out
