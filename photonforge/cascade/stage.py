# -*- coding: utf-8 -*-
"""级联阶段：低分辨率潜空间 -> 高分辨率细化。"""
from __future__ import annotations

from .. import vae


def low_res_generate(velocity_fn, cond, latent_shape, steps: int = 12, sampler=None):
    """低分辨率潜空间生成（512 潜空间）。"""
    from ..flux.base import MockVelocity
    from ..flux.euler import EulerSampler
    sampler = sampler or EulerSampler(steps)
    # 从噪声初始化
    import random
    rng = random.Random(sum(hash(c) % 100000 for c in cond))
    c, h, w = latent_shape
    x = [[[rng.random() for _ in range(w)] for _ in range(h)] for _ in range(c)]
    for t in sampler.schedule():
        x = sampler.step(x, t, velocity_fn, cond)
    return x


def refine(high_res, velocity_fn, cond, steps: int = 4, sampler=None):
    """高分辨率细化：在低分辨率结果基础上再跑少量步数提升细节。"""
    from ..flux.euler import EulerSampler
    sampler = sampler or EulerSampler(steps)
    x = high_res
    for t in sampler.schedule():
        x = sampler.step(x, t, velocity_fn, cond)
    return x
