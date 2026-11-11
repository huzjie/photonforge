# -*- coding: utf-8 -*-
"""adaLN：自适应层归一化。把时间步/条件调制成逐层缩放与平移。"""
from __future__ import annotations

import math


def modulate(cond_vec, hidden_size: int):
    """由条件向量生成 scale/shift 两组参数。

    真实实现里 cond_vec 经一个 SiLU 线性层投影成 2*hidden_size；
    这里用确定性降采样投影模拟，返回 (scale, shift)。
    """
    n = len(cond_vec)
    scale = []
    shift = []
    for i in range(hidden_size):
        # 确定性伪投影：用相邻元素组合，保证零依赖可复现
        v = cond_vec[i % n]
        v2 = cond_vec[(i * 7 + 3) % n]
        scale.append(1.0 + 0.1 * math.tanh(v))
        shift.append(0.1 * math.tanh(v2))
    return scale, shift


def adaln_norm(x, scale, shift, eps: float = 1e-5):
    """带自适应调制与残差门的 LayerNorm。"""
    mean = sum(x) / len(x)
    var = sum((xi - mean) ** 2 for xi in x) / len(x)
    inv = 1.0 / math.sqrt(var + eps)
    return [(xi - mean) * inv * s + b for xi, s, b in zip(x, scale, shift)]


def timestep_embedding(t, hidden_size: int):
    """正弦时间步嵌入（Transformer 位置编码式）。"""
    emb = []
    for i in range(hidden_size // 2):
        freq = 10000.0 ** (-2 * i / hidden_size)
        emb.append(math.sin(t * freq))
        emb.append(math.cos(t * freq))
    return emb[:hidden_size]
