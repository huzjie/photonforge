# -*- coding: utf-8 -*-
"""四阶 Runge-Kutta 采样器：高精度，适合少步采样时的稳定性要求。"""
from __future__ import annotations

from .euler import _guided
from .base import Sampler, add, scale, combine


class RK4Sampler(Sampler):
    name = "rk4"

    def __init__(self, num_steps: int = 12):
        self.num_steps = int(num_steps)

    def step(self, x, t, velocity, cond, uncond=None, guidance: float = 4.5):
        dt = 1.0 / max(self.num_steps, 1)
        k1 = _guided(velocity, x, t, cond, uncond, guidance)
        k2 = _guided(velocity, add(x, scale(k1, dt / 2)), t - dt / 2, cond, uncond, guidance)
        k3 = _guided(velocity, add(x, scale(k2, dt / 2)), t - dt / 2, cond, uncond, guidance)
        k4 = _guided(velocity, add(x, scale(k3, dt)), t - dt, cond, uncond, guidance)
        weighted = add(add(add(scale(k1, 1), scale(k2, 2)), scale(k3, 2)), k4)
        return add(x, scale(weighted, dt / 6))


def create(**kwargs):
    return RK4Sampler(**kwargs)
