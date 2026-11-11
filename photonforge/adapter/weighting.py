# -*- coding: utf-8 -*-
"""多参考图权重策略：softmax 归一、显式权重、等权。"""
from __future__ import annotations


def normalize_weights(weights, n):
    """归一化权重；空则等权。"""
    if not weights:
        return [1.0 / n] * n
    w = list(weights[:n])
    total = sum(w)
    if total == 0:
        return [1.0 / n] * n
    return [x / total for x in w]


def softmax_weights(weights):
    import math
    m = max(weights)
    e = [math.exp(w - m) for w in weights]
    s = sum(e)
    return [x / s for x in e]
