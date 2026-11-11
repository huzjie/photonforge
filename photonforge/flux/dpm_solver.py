# -*- coding: utf-8 -*-
"""DPM-Solver（一阶）采样器：flow 场景下的一阶指数积分近似。"""
from __future__ import annotations

from .euler import _guided
from .base import Sampler, add, scale


class DPMSolverSampler(Sampler):
    name = "dpm_solver"

    def __init__(self, num_steps: int = 12):
        self.num_steps = int(num_steps)

    def step(self, x, t, velocity, cond, uncond=None, guidance: float = 4.5):
        dt = 1.0 / max(self.num_steps, 1)
        v = _guided(velocity, x, t, cond, uncond, guidance)
        return add(x, scale(v, dt))


def create(**kwargs):
    return DPMSolverSampler(**kwargs)
