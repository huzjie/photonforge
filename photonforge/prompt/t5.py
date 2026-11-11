# -*- coding: utf-8 -*-
"""T5 风格文本编码：确定性 token 化 + 分块编码 + 注意力池化。"""
from __future__ import annotations

import hashlib
import math


def tokenize(text: str):
    """极简确定性 token 化（非真实 T5 分词，仅用于离线验证）。"""
    tokens = []
    for ch in text:
        tokens.append(ord(ch))
    return tokens


def encode_chunk(tokens, dim: int = 64):
    """把 token 序列编码为固定维向量（确定性 bag-of-tokens + 位置正弦）。"""
    vec = [0.0] * dim
    for pos, tok in enumerate(tokens):
        for d in range(dim):
            vec[d] += math.sin((tok + 1) * (d + 1) * 0.01) * (1.0 / (pos + 1) ** 0.5)
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def encode_long(text: str, dim: int = 64, chunk_size: int = 512):
    """长文本编码：分块 -> 逐块编码 -> 注意力池化聚合成全局条件向量。"""
    from .chunking import chunk_by_chars
    chunks = chunk_by_chars(text, chunk_size)
    chunk_vecs = [encode_chunk(tokenize(c), dim) for c in chunks]
    return attention_pool(chunk_vecs, dim)


def attention_pool(chunk_vecs, dim: int):
    """注意力池化：按块与首块的相似度加权聚合。"""
    if not chunk_vecs:
        return [0.0] * dim
    if len(chunk_vecs) == 1:
        return chunk_vecs[0]
    first = chunk_vecs[0]
    scores = [1.0]
    for cv in chunk_vecs[1:]:
        dot = sum(a * b for a, b in zip(first, cv))
        scores.append(max(dot, 0.0) + 0.1)
    total = sum(scores)
    out = [0.0] * dim
    for w, cv in zip(scores, chunk_vecs):
        for d in range(dim):
            out[d] += (w / total) * cv[d]
    return out
