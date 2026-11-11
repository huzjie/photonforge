# -*- coding: utf-8 -*-
"""多头自注意力（纯标准库实现）。"""
from __future__ import annotations

import math


def softmax(scores):
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def attention(q, k, v, num_heads: int = 8):
    """缩放点积注意力。q/k/v: [seq][dim]。返回 [seq][dim]。"""
    seq = len(q)
    dim = len(q[0])
    head_dim = dim // num_heads
    out = [[0.0 for _ in range(dim)] for _ in range(seq)]
    for h in range(num_heads):
        s0 = h * head_dim
        for i in range(seq):
            scores = []
            for j in range(seq):
                dot = 0.0
                for d in range(head_dim):
                    dot += q[i][s0 + d] * k[j][s0 + d]
                scores.append(dot / math.sqrt(head_dim))
            w = softmax(scores)
            for d in range(head_dim):
                acc = 0.0
                for j in range(seq):
                    acc += w[j] * v[j][s0 + d]
                out[i][s0 + d] = acc
    return out


def scaled_dot(q_row, k_mat, head_dim: int):
    """单行 Q 对所有 K 的打分（供解耦交叉注意力复用）。"""
    return [sum(q_row[d] * kk[d] for d in range(head_dim)) / math.sqrt(head_dim) for kk in k_mat]
