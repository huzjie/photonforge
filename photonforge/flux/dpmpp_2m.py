# -*- coding: utf-8 -*-
"""DPM++ 2M 采样器：二阶多步，少步数下精度明显优于一阶。"""
from __future__ import annotations

from .euler import _guided
from .base import Sampler, add, scale, combine


class DPMPP2MSampler(Sampler):
    name = "dpmpp_2m"

    def __init__(self, num_steps: int = 12):
        self.num_steps = int(num_steps)
        self._prev_v = None

    def step(self, x, t, velocity, cond, uncond=None, guidance: float = 4.5):
        dt = 1.0 / max(self.num_steps, 1)
        v = _guided(velocity, x, t, cond, uncond, guidance)
        if self._prev_v is None:
            out = add(x, scale(v, dt))
        else:
            out = add(x, scale(combine(v, self._prev_v, 0.5), dt))
        self._prev_v = v
        return out


def create(**kwargs):
    return DPMPP2MSampler(**kwargs)
