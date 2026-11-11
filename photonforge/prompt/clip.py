# -*- coding: utf-8 -*-
"""CLIP 风格对比编码：文本与图像映射到同一空间（简化确定性实现）。"""
from __future__ import annotations

import math


def encode_text(text: str, dim: int = 64):
    from .t5 import tokenize, encode_chunk
    return encode_chunk(tokenize(text), dim)


def encode_image(image, dim: int = 64):
    from ..adapter.reference import encode
    return encode(image, dim)


def similarity(text_vec, image_vec):
    dot = sum(a * b for a, b in zip(text_vec, image_vec))
    nt = math.sqrt(sum(v * v for v in text_vec)) or 1.0
    ni = math.sqrt(sum(v * v for v in image_vec)) or 1.0
    return dot / (nt * ni)


def contrastive_loss(text_vecs, image_vecs, temperature: float = 0.07):
    """简化的 InfoNCE 对比损失（仅示意，真实实现需批量）。"""
    n = len(text_vecs)
    loss = 0.0
    for i in range(n):
        pos = similarity(text_vecs[i], image_vecs[i]) / temperature
        loss -= pos
    return loss / n
