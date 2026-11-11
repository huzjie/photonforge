# -*- coding: utf-8 -*-
"""DiT 基本块：adaLN -> 多头自注意力 -> MLP，双残差。"""
from __future__ import annotations

from . import adaln, attention, mlp


def dit_block(x, cond, num_heads: int = 8, mlp_ratio: float = 4.0):
    """单个 DiT 块。x: [seq][dim]。cond: 条件向量。"""
    dim = len(x[0])
    scale, shift = adaln.modulate(cond, dim)
    normed = [adaln.adaln_norm(tok, scale, shift) for tok in x]
    attn = attention.attention(normed, normed, normed, num_heads)
    x1 = [[a + b for a, b in zip(orig, att)] for orig, att in zip(x, attn)]

    scale2, shift2 = adaln.modulate(cond, dim)
    normed2 = [adaln.adaln_norm(tok, scale2, shift2) for tok in x1]
    ff = [mlp.mlp(tok, hidden_ratio=mlp_ratio) for tok in normed2]
    return [[a + b for a, b in zip(orig, f)] for orig, f in zip(x1, ff)]
