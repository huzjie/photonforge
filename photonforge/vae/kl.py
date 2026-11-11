# -*- coding: utf-8 -*-
"""KL 正则潜空间：约束潜变量接近标准正态，保证生成连续性。"""
from __future__ import annotations

import math


def kl_divergence(mean, logvar):
    """KL(N(mean, var) || N(0, 1))。"""
    return 0.5 * sum(m * m + math.exp(lv) - lv - 1.0 for m, lv in zip(mean, logvar))


def reparameterize(mean, logvar, rng=None):
    """重参数化采样：z = mean + exp(logvar/2) * eps。"""
    import random
    rng = rng or random.Random(0)
    return [m + math.exp(lv / 2) * rng.gauss(0, 1) for m, lv in zip(mean, logvar)]
