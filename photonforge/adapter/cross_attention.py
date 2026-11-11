# -*- coding: utf-8 -*-
"""解耦交叉注意力：文本 K/V 与参考图 K/V 并行注入。"""
from __future__ import annotations

import math

from ..dit.attention import softmax


def decoupled_cross_attention(q, text_kv, ref_kvs, ref_weights, scale: float = 1.0):
    """IP-Adapter 解耦交叉注意力。

    核心思路：Q 同时与「文本 K/V」和「每张参考图 K/V」做注意力，
    参考图作为独立 K/V 并行注入，用 ref_weights 控制各自影响，
    再与文本分支叠加——这样参考图可与文本提示词任意组合、加权。

    q: [seq][dim]
    text_kv: (text_k, text_v)，各 [seq][dim]
    ref_kvs: [(ref_k, ref_v), ...] 每张参考图一对
    ref_weights: 每张参考图权重
    """
    head_dim = len(q[0])
    # 文本分支
    text_out = _attend(q, text_kv[0], text_kv[1])
    # 参考图分支
    total_w = sum(ref_weights) if ref_weights else 0.0
    ref_out = None
    for (rk, rv), w in zip(ref_kvs, ref_weights):
        o = _attend(q, rk, rv)
        if ref_out is None:
            ref_out = [[w * v for v in row] for row in o]
        else:
            ref_out = [[a + w * b for a, b in zip(r1, r2)] for r1, r2 in zip(ref_out, o)]
    if ref_out is None:
        return text_out
    # 归一化参考图分支 + scale 控制，与文本分支相加
    norm = 1.0 / max(total_w, 1e-6)
    return [[a + scale * b * norm for a, b in zip(t, r)] for t, r in zip(text_out, ref_out)]


def _attend(q, k, v):
    out = []
    for qrow in q:
        scores = [sum(a * b for a, b in zip(qrow, kk)) / math.sqrt(max(len(qrow), 1)) for kk in k]
        w = softmax(scores)
        out_row = [0.0] * len(v[0])
        for j, wj in enumerate(w):
            for d in range(len(out_row)):
                out_row[d] += wj * v[j][d]
        out.append(out_row)
    return out


def make_ref_kv(feats):
    """把参考图特征构造成 K/V 对（K = V = 特征，简化）。"""
    k = [list(f) for f in feats]
    v = [list(f) for f in feats]
    return k, v
