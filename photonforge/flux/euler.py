# -*- coding: utf-8 -*-
"""一阶 Euler 采样器：x_{t-dt} = x_t + v * dt。最简单、最通用。"""
from __future__ import annotations

from .base import Sampler, add, scale


class EulerSampler(Sampler):
    name = "euler"

    def step(self, x, t, velocity, cond, uncond=None, guidance: float = 4.5):
        dt = 1.0 / max(self.num_steps, 1)
        v = _guided(velocity, x, t, cond, uncond, guidance)
        return add(x, scale(v, dt))


def _guided(velocity, x, t, cond, uncond, guidance):
    from .base import add, sub, scale, combine
    v = velocity(x, t, cond)
    if uncond is None or guidance <= 0:
        return v
    vu = velocity(x, t, uncond)
    # 分类器无关引导：v_cfg = v_uncond + guidance * (v_cond - v_uncond)
    return add(vu, scale(sub(v, vu), guidance))


def create(**kwargs):
    return EulerSampler(**kwargs)
