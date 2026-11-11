# -*- coding: utf-8 -*-
"""二阶 Heun（改进 Euler）采样器：预测-校正，精度高、步数少时更稳。"""
from __future__ import annotations

from .euler import _guided
from .base import Sampler, add, scale, combine


class HeunSampler(Sampler):
    name = "heun"

    def __init__(self, num_steps: int = 12):
        self.num_steps = int(num_steps)

    def step(self, x, t, velocity, cond, uncond=None, guidance: float = 4.5):
        dt = 1.0 / max(self.num_steps, 1)
        v1 = _guided(velocity, x, t, cond, uncond, guidance)
        x_mid = add(x, scale(v1, dt))
        v2 = _guided(velocity, x_mid, t - dt, cond, uncond, guidance)
        return add(x, scale(combine(v1, v2, 0.5), dt))


def create(**kwargs):
    return HeunSampler(**kwargs)
