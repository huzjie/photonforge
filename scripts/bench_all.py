# -*- coding: utf-8 -*-
"""全量基准：不同步数/采样器对比。"""
import time
from photonforge.flux.euler import EulerSampler
from photonforge.flux.heun import HeunSampler
from photonforge.flux.rk4 import RK4Sampler
from photonforge.flux.base import MockVelocity

target = 1.0
for sampler_cls in (EulerSampler, HeunSampler, RK4Sampler):
    for steps in (4, 8, 16, 20):
        s = sampler_cls(steps)
        x = 0.0
        t0 = time.perf_counter()
        for t in s.schedule():
            x = s.step(x, t, MockVelocity(target), "c")
        dt = (time.perf_counter() - t0) * 1000
        print(f"{sampler_cls.name:<12} steps={steps:<3} x={x:.4f} {dt:.2f}ms")
